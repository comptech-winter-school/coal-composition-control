from types import SimpleNamespace

import torch

from src.base import BasePredictor, InstanceSegmentationCoal
from src.instance_segmentation.yolact_utils import eval
from src.instance_segmentation.yolact_utils.layers.output_utils import postprocess
from src.instance_segmentation.yolact_utils.yolact import Yolact
from src.utils import get_contours


def get_yolact(weights):
    model = Yolact()
    map_location = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
    model.load_weights(weights, map_location=map_location)
    model = model.to(map_location)
    return model

def get_args(score_threshold, top_k):
    args_dict = {
        'crop': True,
        'score_threshold': score_threshold,
        'display_lincomb': False,
        'top_k': top_k,
        'eval_mask_branch': True,
    }
    return SimpleNamespace(**args_dict)


class YolactPredictor(BasePredictor):
    def __init__(self, weights, score_threshold=0.1, top_k=15, width=None, height=None):
        self.model = get_yolact(weights)
        self.args = get_args(score_threshold, top_k)
        self.width = width
        self.height = height

    @torch.no_grad()
    def predict(self, img):
        self.model.eval()
        preds = eval.evalimage(self.model, img)
        height, width = img.shape[:2]
        height = self.height if self.height is not None else height
        width = self.width if self.width is not None else width
        preds = postprocess(
            preds, width, height,
            visualize_lincomb=self.args.display_lincomb,
            crop_masks=self.args.crop,
            score_threshold=self.args.score_threshold
        )
        idx = preds[1].argsort(0, descending=True)[:self.args.top_k]
        masks = preds[3][idx]
        masks = masks.detach().cpu().numpy()
        masks = [(mask * 255).astype('uint8') for mask in masks]
        return [InstanceSegmentationCoal(get_contours(mask)[0]) for mask in masks]

