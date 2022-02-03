from pathlib import Path
from typing import Union, List

import albumentations as albu
import cv2
import numpy as np
import segmentation_models_pytorch as smp
import torch
from numpy.typing import NDArray

from constants import DATA_DIR, WEIGHTS_DIR
from src.base import BasePredictor, InstanceSegmentationCoal
from src.utils import get_device


class SemanticSegmentation(BasePredictor):
    def __init__(
            self,
            weights: Union[Path, str],
            thr_mask: float = 0.7,
            device: str = None):

        self.model = torch.load(weights)
        self.model.eval()

        self.device = get_device(device=device)
        self.preprocessing_fn = smp.encoders.get_preprocessing_fn('efficientnet-b0', 'imagenet')

        self.segm_th_mask = thr_mask
        self.mask = None
        self.rectangles = None

        self.contours = []

    def get_contours(self):
        self.mask = cv2.morphologyEx(self.mask,
                                     cv2.MORPH_OPEN,
                                     cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)),
                                     iterations=2)

        contours, hierarchy = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        [self.contours.append(InstanceSegmentationCoal(cnt)) for cnt in contours if cv2.contourArea(cnt) > 150]


    @torch.no_grad()
    def predict(self, img: NDArray) -> List[InstanceSegmentationCoal]:
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = albu.Compose([albu.Lambda(image=self.preprocessing_fn)])(image=image)['image']
        image = image.transpose(2, 0, 1).astype('float32')

        x_tensor = torch.from_numpy(image).to(self.device).unsqueeze(0)
        pr_mask = self.model.predict(x_tensor).squeeze(0).cpu().numpy()
        pr_mask = pr_mask.transpose(1, 2, 0)

        self.mask = np.where(pr_mask[:, :, 2:3] > self.segm_th_mask, 255, 0).astype(dtype=np.uint8)

        self.get_contours()

        return self.contours


if __name__ == '__main__':
    orig_image = cv2.imread(str(DATA_DIR / 'few_data_split' / 'train' / '20210712_141048_857A_ACCC8EAF31F3_0.jpg'))
    semantic_segmentation = SemanticSegmentation(WEIGHTS_DIR / 'unet_efficientnet-b0.pth')

    coals = semantic_segmentation.predict(orig_image)
    print([coal.get_fraction() for coal in coals])
