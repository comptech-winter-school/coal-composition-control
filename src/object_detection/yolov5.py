from pathlib import Path
from typing import Union, List

import torch
from numpy.typing import NDArray

from src.base import BasePredictor, DetectionCoal
from src.utils import get_device


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
        """
        Class for predict coal fraction with YOLOV5 (https://github.com/ultralytics/yolov5)

        :param weights: path to .pt file
        :param box_conf_th: segmentation in bounding box with confidence > threshold
        :param nms_th: nms threshold (https://pytorch.org/vision/main/generated/torchvision.ops.nms.html)
        :param amp: use automatic mixed precision to speed up inference at the small cost of accuracy
        :param size: before inference resize image to this size, after rescale predict
        :param device: 'cpu', 'cuda:0' etc. (https://pytorch.org/docs/stable/tensor_attributes.html#torch.torch.device)
        """
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
        """
        Find coals on image

        :param img: image with coals; image = cv2.imread(path/to/image)
        :return: list of DetectionCoals from bbox
        """
        img = img[..., ::-1]
        prediction = self.model(img, size=self.size)
        boxes = prediction.xyxy[0].detach().cpu().numpy()
        return [DetectionCoal(box[:4]) for box in boxes]
