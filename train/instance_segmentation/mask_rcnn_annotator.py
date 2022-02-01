"""
Create VGG json from Mask R-CNN predict
"""
from pathlib import Path
from typing import Dict, Union

import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from numpy.typing import NDArray

from constants import DATA_DIR, WEIGHTS_DIR
from src.utils import get_device, get_model
from train.converters.mask_to_vgg import masks2vgg


class Annotator:

    def __init__(
            self,
            weights: Union[Path, str],
            box_conf_th: float = 0.5,
            nms_th: float = 0.2,
            segmentation_th: float = 0.7,
            device: str = None
    ):
        self.device = get_device(device=device)
        self.model = get_model(weights, box_conf_th, nms_th, self.device)
        self.segmentation_th = torch.Tensor([segmentation_th])
        self.segmentation_th.to(self.device)

    def names_and_masks(self, folder: Path) -> Dict[str, NDArray]:
        names_masks = {}
        for image_path in folder.glob('*'):
            img = cv2.imread(str(image_path))
            if img is None:
                print(f'skip {image_path}')
                continue
            img = transforms.ToTensor()(img)
            img.to(self.device)

            prediction = self.model([img])
            masks = torch.squeeze(prediction[0]['masks'])
            masks = (masks > self.segmentation_th)
            names_masks[image_path.name] = np.array(masks)
        return names_masks

    def to_vgg(self, folder: Union[Path, str], save_path: Union[str, Path]) -> None:
        names_and_masks = self.names_and_masks(folder=Path(folder))
        masks2vgg(names_and_masks=names_and_masks, save_path=save_path)


if __name__ == '__main__':
    annotator = Annotator(
        weights=WEIGHTS_DIR / 'mask_rcnn.pth',
        box_conf_th=0.7,
        nms_th=0.2,
        segmentation_th=0.7
    )
    annotator.to_vgg(
        folder=DATA_DIR / 'few_data',
        save_path=DATA_DIR / 'output.json'
    )
