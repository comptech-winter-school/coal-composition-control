from pathlib import Path
from typing import Union, List, Tuple

from numpy.typing import NDArray

from src.base import BasePredictor, InstanceSegmentationCoal
from src.utils import get_contours
from train.converters.vgg_to_mask import vgg2dict, dict2mask
from train.eval_utils import colour_mask_to_binary_masks


class DummyPredictor(BasePredictor):

    def __init__(
            self,
            vgg_json: Union[Path, str],
            ordered_names: List[str],
            cut_params: Tuple[int, int, int, int]
    ):
        self.annotations = vgg2dict(vgg_json=vgg_json, cut_params=cut_params)
        self.ordered_names = ordered_names
        self.cut_params = cut_params
        self.count = 0

    def reset_count(self):
        self.count = 0

    def predict(self, img: NDArray) -> List[InstanceSegmentationCoal]:
        """
        Return image annotation as predict
        """
        _, _, w, h = self.cut_params
        img_name = self.ordered_names[self.count]
        self.count += 1

        if img_name == self.ordered_names[-1]:
            self.reset_count()

        masks = dict2mask(image_name=img_name, mask_dict=self.annotations, mask_width=w, mask_height=h)
        masks = colour_mask_to_binary_masks(masks)
        masks = ((mask * 255).astype('uint8') for mask in masks)
        return [InstanceSegmentationCoal(get_contours(mask)[0]) for mask in masks]
