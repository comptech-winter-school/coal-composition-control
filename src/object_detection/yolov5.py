from pathlib import Path
from typing import Union, List

import cv2
import torch
from numpy.typing import NDArray

from constants import EXAMPLE_IMG, WEIGHTS_DIR
from src.base import BasePredictor, DetectionCoal
from src.utils import get_device, plot_coals_contours_on_img


def get_yolov5(weights, box_conf_th: float, nms_th: float, amp: bool, device):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights, device=device)  # local model
    model.conf = box_conf_th  # NMS confidence threshold
    model.iou = nms_th        # NMS IoU threshold
    model.amp = amp           # Automatic Mixed Precision (AMP) inference
    model.eval()
    return model


class YOLOv5(BasePredictor):

    def __init__(
            self,
            weights: Union[Path, str],
            box_conf_th: float = 0.5,
            nms_th: float = 0.2,
            amp: bool = True,
            size: int = 1280,
            device: str = None,
    ):
        self.device = get_device(device=device)
        self.model = get_yolov5(
            weights=weights,
            box_conf_th=box_conf_th,
            nms_th=nms_th,
            amp=amp,
            device=self.device
        )
        self.size = size

    @torch.no_grad()
    def predict(self, img: NDArray) -> List[DetectionCoal]:
        img = img[..., ::-1]
        prediction = self.model(img, size=self.size)
        boxes = prediction.xyxy[0].detach().cpu().numpy()
        return [DetectionCoal(box[:4]) for box in boxes]


if __name__ == '__main__':
    image = cv2.imread(str(EXAMPLE_IMG))
    yolo = YOLOv5(
        weights=WEIGHTS_DIR / 'yolov5s6.pt',
        box_conf_th=0.2,
        nms_th=0.2,
        amp=True,
        size=1280,
        device=None
    )

    coals = yolo.predict(image)
    print([coal.get_fraction() for coal in coals])

    if coals:
        cv2.imshow('Contours', plot_coals_contours_on_img(image, coals))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
