from pathlib import Path
from typing import Union

import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from numpy.typing import NDArray

import sys
FILE = Path(__file__).resolve()
ROOT = FILE.parents[2]  # root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

from src.base import BasePredictor, InstanceSegmentationCoals


class MaskRCNN(BasePredictor):

    def __init__(
            self,
            weights: Union[Path, str],
            box_conf_th: float = 0.5,
            nms_th: float = 0.2,
            segmentation_th: float = 0.7,
            device: str = None
    ):
        self.device = self.get_device(device=device)
        self.model = self.get_model(weights, box_conf_th, nms_th)
        self.segmentation_th = torch.Tensor([segmentation_th])
        self.segmentation_th.to(self.device)

    @staticmethod
    def get_device(device: str):
        if device is None:
            return torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        return torch.device(device)

    @staticmethod
    def get_model(weights, box_conf_th: float, nms_th: float):
        model = torch.load(weights, map_location=torch.device('cpu'))
        model.roi_heads.score_thresh = box_conf_th
        model.roi_heads.nms_thresh = nms_th
        model.eval()
        return model

    @staticmethod
    def rectangle(mask):
        contours, _ = cv2.findContours((mask * 255).astype('uint8'), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return cv2.minAreaRect(contours[0])

    @torch.no_grad()
    def predict(self, img: NDArray) -> InstanceSegmentationCoals:
        img = transforms.ToTensor()(img)
        img.to(self.device)

        prediction = self.model([img])
        masks = torch.squeeze(prediction[0]['masks'])
        masks = np.array(masks > self.segmentation_th)
        rectangles = [self.rectangle(mask) for mask in masks]
        return InstanceSegmentationCoals(rectangles=rectangles)


if __name__ == '__main__':
    img = cv2.imread(str(Path.cwd().parents[1] / 'few_data' / '20210712_141048_857A_ACCC8EAF31F3_0.jpg'))
    model = MaskRCNN('/home/ji411/Downloads/1/mask-rcnn.pth')
    print(model.predict(img).get_fraction())
