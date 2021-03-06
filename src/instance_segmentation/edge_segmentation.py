from pathlib import Path
from typing import Union, List, Tuple

import albumentations as albu
import cv2
import numpy as np
import segmentation_models_pytorch as smp
import torch
from numpy.typing import NDArray

from src.base import BasePredictor, InstanceSegmentationCoal
from src.utils import get_device, get_contours


def get_unet(weights, device):

    CLASSES = ['coal', 'bound', 'background']
    model = smp.Unet(
        encoder_name='efficientnet-b0',
        encoder_weights=None,
        classes=len(CLASSES),
        activation='softmax',
    )
    model_state_dict = torch.load(weights, map_location=device)
    model.load_state_dict(model_state_dict)
    model = model.to(device)
    model.eval()
    return model

def check_cut_params(cut_params, stride: int = 32):
    if cut_params is None:
        return None
    if cut_params[2] % stride != 0 or cut_params[3] % stride != 0:
        raise ValueError(f'size must be divisible to {stride}')
    return cut_params


class EdgeSegmentation(BasePredictor):
    """
    :param weights: path to the model weights.
    :param segm_th_mask: Degree of confidence that pixel is coal. Range [0.0, 1.0].
    :param contour_area_min: Minimal area threshold in pixels to assume that selected contour is coal.
    :param width: Width of the input image, divisible to 32, don't resize if None or height is None.
    :param height: Height of the input image, divisible to 32, don't resize if None or width is None.
    :param device: Device where model runs. 
    """

    def __init__(
            self,
            weights: Union[Path, str],
            segm_th_mask: float = 0.1,
            contour_area_min: int = 150,
            cut_params: Tuple[int, int, int, int] = (0, 0, 1280, 512),
            device: str = None
    ):

        self.device = get_device(device=device)
        self.model = get_unet(weights, self.device)
        self.preprocessing_fn = smp.encoders.get_preprocessing_fn('efficientnet-b0', 'imagenet')

        self.cut_params = check_cut_params(cut_params, stride=32)
        self.segm_th_mask = segm_th_mask
        self.contour_area_min = contour_area_min

    def image_preprocess(self, img: NDArray) -> torch.Tensor:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if self.cut_params is not None:
            x, y, w, h = self.cut_params
            img = img[y:y + h, x:x + w]
        img = albu.Compose([albu.Lambda(image=self.preprocessing_fn)])(image=img)['image']
        img = img.transpose(2, 0, 1).astype('float32')
        return torch.from_numpy(img).to(self.device).unsqueeze(0)

    @torch.no_grad()
    def predict(self, img: NDArray) -> List[InstanceSegmentationCoal]:
        x_tensor = self.image_preprocess(img=img)

        pr_mask = self.model.predict(x_tensor).squeeze(0).cpu().numpy()
        pr_mask = pr_mask.transpose(1, 2, 0)

        mask = np.where(pr_mask[:, :, 2:3] > self.segm_th_mask, 255, 0).astype(dtype=np.uint8)
        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)),
            iterations=2
        )

        contours = get_contours(mask)
        return [InstanceSegmentationCoal(cnt) for cnt in contours if cv2.contourArea(cnt) > self.contour_area_min]
