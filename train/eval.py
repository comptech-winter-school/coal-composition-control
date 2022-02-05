from pathlib import Path
from typing import Tuple

import cv2
import numpy as np

from constants import WEIGHTS_DIR, DATA_DIR
from src.base import InstanceSegmentationCoal, DetectionCoal, BasePredictor
from src.instance_segmentation.edge_segmentation import EdgeSegmentation
from src.instance_segmentation.mask_rcnn import MaskRCNN
from src.instance_segmentation.yolact import YolactPredictor
from src.object_detection.yolov5 import YOLOv5
from src.utils import get_contours
from train.converters.vgg_to_mask import vgg2dict
from train.eval_utils import colour_mask_to_binary_masks, extract_bboxes, \
    compute_ap_range, compute_matches


def contours_to_boxes_and_mask(contours, height, width):
    mask = np.zeros((height, width))
    for contour_num, contour in enumerate(contours):
        contour = np.array(contour, dtype=np.int32)
        cv2.fillPoly(mask, [contour], color=contour_num + 1)
    mask = colour_mask_to_binary_masks(mask)
    mask = np.transpose(mask, (1, 2, 0))
    boxes = extract_bboxes(mask)
    return boxes, mask

def coals_contours(model, image):
    coals = model.predict(image)

    if not coals:
        return None
    if isinstance(coals[0], InstanceSegmentationCoal):
        contours = [coal.contour for coal in coals]
    elif isinstance(coals[0], DetectionCoal):
        contours = []
        for coal in coals:
            xmin, ymin, xmax, ymax = coal.box
            contour = [[xmax, ymax], [xmax, ymin], [xmin, ymin], [xmin, ymax]]
            contours.append(contour)
    else:
        raise ValueError('You model should return List[Coal]')
    return contours

def boxes_masks_class_scores(contours, height, width):
    boxes, masks = contours_to_boxes_and_mask(
        contours=contours,  # self.annotations[image_path.name],
        height=height,
        width=width
    )
    return boxes, masks, np.ones(len(boxes)), np.ones(len(boxes))

def mask2size(mask):
    mask = (mask * 255).astype('uint8')
    contours = get_contours(mask)
    if contours:
        return InstanceSegmentationCoal(get_contours(mask)[0]).get_fraction()

class Evaluator:

    def __init__(self, images_dir: Path, vgg_json: Path, cut_params: Tuple[int, int, int, int] = None) -> None:
        self.images_dir = images_dir
        self.annotations = vgg2dict(vgg_json=vgg_json)
        self.cut_params = cut_params

    def ap(self, model: BasePredictor) -> float:

        for image_path in self.images_dir.glob('*'):
            image = cv2.imread(str(image_path))
            if self.cut_params is not None:
                x, y, w, h = self.cut_params
                image = image[y:y + h, x:x + w]
            height, width = image.shape[:2]
            contours = coals_contours(model, image)
            if contours is None:
                continue

            gt_boxes, gt_masks, gt_cls, _ = boxes_masks_class_scores(
                contours=self.annotations[image_path.name],
                height=height,
                width=width
            )

            pred_boxes, pred_masks, pred_cls, pred_scores = boxes_masks_class_scores(
                contours=contours,  # self.annotations[image_path.name],
                height=height,
                width=width
            )

            return compute_ap_range(
                gt_boxes, gt_cls, gt_masks,
                pred_boxes, pred_cls, pred_scores, pred_masks,
            )

    def mae(self, model: BasePredictor) -> float:

        for image_path in self.images_dir.glob('*'):
            image = cv2.imread(str(image_path))
            if self.cut_params is not None:
                x, y, w, h = self.cut_params
                image = image[y:y + h, x:x + w]
            height, width = image.shape[:2]
            contours = coals_contours(model, image)
            if contours is None:
                continue

            gt_boxes, gt_masks, gt_cls, _ = boxes_masks_class_scores(
                contours=self.annotations[image_path.name],
                height=height,
                width=width
            )

            pred_boxes, pred_masks, pred_cls, pred_scores = boxes_masks_class_scores(
                contours=contours,  # self.annotations[image_path.name],
                height=height,
                width=width
            )

            gt_match, _, _ = compute_matches(
                gt_boxes, gt_cls, gt_masks,
                pred_boxes, pred_cls, pred_scores, pred_masks,
                iou_threshold=0.5, score_threshold=0.1
            )

            pred_masks = np.transpose(pred_masks, (2, 0, 1))
            gt_masks = np.transpose(gt_masks, (2, 0, 1))

            abs_error = 0
            for match, gt_mask in zip(gt_match, gt_masks):
                match = int(match)
                pred_size = 0
                if match != -1:
                    pred_mask = pred_masks[match]
                    pred_size = mask2size(pred_mask)
                gt_size = mask2size(gt_mask)
                abs_error += abs(gt_size - pred_size)
            return abs_error / len(gt_masks)


if __name__ == '__main__':
    mask_rcnn = MaskRCNN(WEIGHTS_DIR / 'mask_rcnn.pth')
    edge_segmentation = EdgeSegmentation(WEIGHTS_DIR / 'edge_segmentation.pth')
    yolo = YOLOv5(weights=WEIGHTS_DIR / 'yolov5s6.pt')
    yolact = YolactPredictor(weights=WEIGHTS_DIR / 'yolact.pth')

    evaluator = Evaluator(
        images_dir=DATA_DIR / 'few_data_split' / 'few_data_val',
        vgg_json=DATA_DIR / 'few_data_split' / 'few_data_val.json',
        cut_params=(0, 0, 1280, 512)
    )

    print('Mask R-CNN:')
    evaluator.ap(model=mask_rcnn)
    print('MAE:', evaluator.mae(model=mask_rcnn))
    print()

    print('U-Net:')
    evaluator.ap(model=edge_segmentation)
    print('MAE:', evaluator.mae(model=edge_segmentation))
    print()

    print('YOLOv5:')
    evaluator.ap(model=yolo)
    print('MAE:', evaluator.mae(model=yolo))
    print()

    print('Yolact:')
    evaluator.ap(model=yolact)
    print('MAE:', evaluator.mae(model=yolact))
    print()


