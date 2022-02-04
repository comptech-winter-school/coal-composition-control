import cv2
import numpy as np
import torch


def get_device(device: str):
    if device is None:
        return torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    return torch.device(device)


def get_contours(mask):
    contours, _ = cv2.findContours(mask,  cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours


def visualize_semantic_segmentation(img_from_camera, pred):
    return np.where(
        pred > 240,
        cv2.addWeighted(img_from_camera, 0.4, pred, 0.6, 1.0),
        img_from_camera,
    )


def plot_coals_contours_on_img(img, coals: list):
    img_with_contours = np.copy(img)
    for coal2plot in coals:
        coal2plot.plot_on(img_with_contours)
    return img_with_contours


def setup_model(segmentation_type):
    if segmentation_type == 'semantic':
        model = EdgeSegmentation(
        weights=WEIGHTS_DIR / 'best_model3.pth',
        segm_th_mask=0.8)

    elif segmentation_type == 'mask_rcnn':
        model = MaskRCNN(
        weights=WEIGHTS_DIR / 'mask_rcnn.pth',
        box_conf_th=0.7,
        nms_th=0.2,
        segmentation_th=0.7,
        device='cuda:0')
    elif segmentation_type == 'yolov5':
        model = None
        return
    else:
        model = None
        return
    return model


def get_perspective_transform(image,
                              lhs_rectangle=np.float32([[690, 0], [1450, 0], [360, 1080], [940, 1020]]),
                              rhs_rectangle=np.float32([[0, 0], [1920, 0], [0, 1080], [1920, 1080]]),
                              final_size=(1920, 1080)):
    # [1 2] -> [1 2]
    # [3 4] -> [3 4]
    M = cv2.getPerspectiveTransform(lhs_rectangle, rhs_rectangle)
    dst = cv2.warpPerspective(image, M, final_size)
    return dst

