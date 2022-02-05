from pathlib import Path
from typing import Union, List

import cv2
import torch
import torchvision.transforms as transforms
from numpy.typing import NDArray

from constants import EXAMPLE_IMG, WEIGHTS_DIR
from src.base import BasePredictor, InstanceSegmentationCoal
from src.utils import get_device, get_contours


def get_mask_rcnn(weights, box_conf_th: float, nms_th: float, device):
    model = torch.load(weights, map_location=device)
    model.roi_heads.score_thresh = box_conf_th
    model.roi_heads.nms_thresh = nms_th
    model.eval()
    return model

class MaskRCNN(BasePredictor):

    def __init__(
            self,
            weights: Union[Path, str],
            box_conf_th: float = 0.5,
            nms_th: float = 0.2,
            segmentation_th: float = 0.7,
            device: str = None
    ):
        """
        Class for predict coal fraction with Mask R-CNN
        (https://pytorch.org/vision/stable/_modules/torchvision/models/detection/mask_rcnn.html)

        :param weights: path to .pth file
        :param box_conf_th: segmentation in bounding box with confidence > threshold
        :param nms_th: nms threshold (https://pytorch.org/vision/main/generated/torchvision.ops.nms.html)
        :param segmentation_th: if the confidence > threshold accept pixel as part of coal
        :param device: 'cpu', 'cuda:0' etc. (https://pytorch.org/docs/stable/tensor_attributes.html#torch.torch.device)
        """
        self.device = get_device(device=device)
        self.model = get_mask_rcnn(weights, box_conf_th, nms_th, self.device)
        self.segmentation_th = torch.Tensor([segmentation_th]).to(self.device)

    @torch.no_grad()
    def predict(self, img: NDArray) -> List[InstanceSegmentationCoal]:
        """
        Find coals on image

        :param img: image with coals; image = cv2.imread(path/to/image)
        :return: list of InstanceSegmentationCoals from segmented contours
        """
        img = transforms.ToTensor()(img)
        img = img.to(self.device)

        prediction = self.model([img])
        masks = torch.squeeze(prediction[0]['masks'])
        masks = masks > self.segmentation_th
        masks = masks.detach().cpu().numpy()
        masks = ((mask * 255).astype('uint8') for mask in masks)
        return [InstanceSegmentationCoal(get_contours(mask)[0]) for mask in masks]


if __name__ == '__main__':
    image = cv2.imread(str(EXAMPLE_IMG))
    mask_rcnn = MaskRCNN(WEIGHTS_DIR / 'mask_rcnn.pth')

    coals = mask_rcnn.predict(image)
    print([coal.get_fraction() for coal in coals])

    if coals:
        cv2.imshow('Contours', coals[0].plot_on(image))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
