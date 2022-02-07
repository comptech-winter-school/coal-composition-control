import warnings
warnings.simplefilter("ignore", UserWarning)

from pathlib import Path
from typing import Tuple, Union
from numpy.typing import NDArray

import cv2
import numpy as np

from constants import WEIGHTS_DIR, DATA_DIR
from src.base import InstanceSegmentationCoal, DetectionCoal, BasePredictor
from src.instance_segmentation.edge_segmentation import EdgeSegmentation
from src.instance_segmentation.mask_rcnn import MaskRCNN
from src.instance_segmentation.yolact import YolactPredictor
from src.object_detection.yolov5 import YOLOv5
from src.utils import get_contours, plot_coals_contours_on_img
from train.converters.vgg_to_mask import vgg2dict
from train.eval_utils import colour_mask_to_binary_masks, extract_bboxes, \
    compute_ap_range, compute_matches
from train.DummyPredictor import DummyPredictor
from time import time

def contours_to_boxes_and_mask(contours, height, width):
    mask = np.zeros((height, width))
    for contour_num, contour in enumerate(contours):
        contour = np.array(contour, dtype=np.int32)
        cv2.fillPoly(mask, [contour], color=contour_num + 1)
    mask = colour_mask_to_binary_masks(mask)
    mask = np.transpose(mask, (1, 2, 0))
    boxes = extract_bboxes(mask)
    return boxes, mask

def coals_contours(model, image, output_image_path: Path = None):
    coals = model.predict(image)

    if output_image_path is not None:
        cv2.imwrite(img=plot_coals_contours_on_img(img=image, coals=coals),
                    filename=str(output_image_path))

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

    def __init__(
            self,
            images_dir: Path,
            vgg_json: Path,
            cut_params: Tuple[int, int, int, int] = None,
            ap_iou_thresholds: NDArray = None
    ) -> None:
        self.images_dir = images_dir
        self.annotations = vgg2dict(vgg_json=vgg_json, cut_params=cut_params)
        self.cut_params = cut_params
        self.ap_iou_thresholds = ap_iou_thresholds if ap_iou_thresholds is not None else np.arange(0.5, 1.0, 0.05)

    def ap(self, model: BasePredictor, output_images_dir: Path = None) -> Tuple[NDArray, float]:

        ap = np.zeros(11)
        start_time = time()

        images = list(self.images_dir.glob('*'))

        for image_path in images:
            image = cv2.imread(str(image_path))
            if self.cut_params is not None:
                x, y, w, h = self.cut_params
                image = image[y:y + h, x:x + w]
            height, width = image.shape[:2]
            contours = coals_contours(model, image, output_image_path=output_images_dir / image_path.name)
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

            ap += compute_ap_range(
                gt_boxes, gt_cls, gt_masks,
                pred_boxes, pred_cls, pred_scores, pred_masks,
                verbose=False, iou_thresholds=self.ap_iou_thresholds
            )
        wall_time = time() - start_time
        fps = len(images) / wall_time
        return ap / len(list(self.images_dir.glob('*'))), fps

    def mae(self, model: BasePredictor) -> float:

        abs_error = 0
        count = 0

        for image_path in self.images_dir.glob('*'):
            image = cv2.imread(str(image_path))
            if self.cut_params is not None:
                x, y, w, h = self.cut_params
                image = image[y:y + h, x:x + w]
            height, width = image.shape[:2]
            contours = coals_contours(model, image, output_image_path=None)
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

            for match, gt_mask in zip(gt_match, gt_masks):
                match = int(match)
                pred_size = 0
                if match != -1:
                    pred_mask = pred_masks[match]
                    pred_size = mask2size(pred_mask)
                gt_size = mask2size(gt_mask)
                abs_error += abs(gt_size - pred_size)
                count += len(gt_masks)
        return abs_error / count

    def eval_results(self, name: str, model: BasePredictor,
                     txt_file: Union[Path, str] = None, output_images_dir: Path = None) -> None:

        if not output_images_dir.exists():
            output_images_dir.mkdir(parents=True)

        AP, fps = self.ap(model=model, output_images_dir=output_images_dir)
        AP, iou_thresholds = AP.tolist(), self.ap_iou_thresholds.tolist()
        fps = round(fps, 3)

        text = f'{name}: \nFPS: {fps} \n'
        for iou_threshold, ap in zip(iou_thresholds, AP):
            text += "AP @{:.2f}:\t {:.3f} \n".format(iou_threshold, ap)
        text += "AP @{:.2f}-{:.2f}:\t {:.3f} \n".format(iou_thresholds[0], iou_thresholds[-1], AP[-1])
        text += f'MAE: {self.mae(model=model)} \n\n'

        if txt_file is not None:
            with open(txt_file, 'w+', encoding='utf-8') as f:
                f.write(text)
        else:
            print(text)

        print(f'{name} evaluation done')


def eval_all(
        images_dir: Path,
        vgg_json: Path,
        output: Path,
        cut_params: Tuple[int, int, int, int] = (544, 0, 1280, 568)
) -> None:

    mask_rcnn = MaskRCNN(WEIGHTS_DIR / 'mask_rcnn.pth')
    edge_segmentation = EdgeSegmentation(WEIGHTS_DIR / 'edge_segmentation.pth')
    yolo = YOLOv5(weights=WEIGHTS_DIR / 'yolov5s6.pt')
    yolact = YolactPredictor(weights=WEIGHTS_DIR / 'yolact.pt')

    dummy = DummyPredictor(
        vgg_json=vgg_json,
        ordered_names=[i.name for i in images_dir.glob('*')],
        cut_params=cut_params
    )

    evaluator = Evaluator(
        images_dir=images_dir,
        vgg_json=vgg_json,
        cut_params=cut_params
    )

    evaluator.eval_results(
        name='Mask R-CNN',
        model=mask_rcnn,
        txt_file=output / 'Mask R-CNN' / 'results.txt',
        output_images_dir=output / 'Mask R-CNN'
    )

    evaluator.eval_results(
        name='U-Net',
        model=edge_segmentation,
        txt_file=output / 'U-Net' / 'results.txt',
        output_images_dir=output / 'U-Net'
    )

    evaluator.eval_results(
        name='YOLOv5',
        model=yolo,
        txt_file=output / 'YOLOv5' / 'results.txt',
        output_images_dir=output / 'YOLOv5'
    )

    evaluator.eval_results(
        name='YOLACT',
        model=yolact,
        txt_file=output / 'YOLACT' / 'results.txt',
        output_images_dir=output / 'YOLACT'
    )

    evaluator.eval_results(
        name='Original',
        model=dummy,
        txt_file=output / 'Original' / 'results.txt',
        output_images_dir=output / 'Original'
    )


if __name__ == '__main__':
    eval_all(
        images_dir=DATA_DIR / 'test_frames',
        vgg_json=DATA_DIR / 'test.json',
        output=DATA_DIR / 'output'
    )
