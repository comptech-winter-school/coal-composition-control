import sys
# определить папку для yolact в структуре
import eval
import layers
from data import COCODetection, get_label_map, MEANS, COLORS
from yolact import Yolact
from utils.augmentations import BaseTransform, FastBaseTransform, Resize
from layers.output_utils import postprocess, undo_image_transformation

import cv2
import torch
import numpy as np
from PIL import Image
from pathlib import Path
from types import SimpleNamespace

from constants import EXAMPLE_IMG, WEIGHTS_DIR
from src.base import BasePredictor, InstanceSegmentationCoal
from src.utils import get_device, get_contours


class YolactPredictor(BasePredictor):
    def __init__(self, weights_path, score_threshold=0.15, top_k=15, cuda=False):
        self.model = self.get_model(weights_path, cuda=cuda)
        args_dict = {'crop': False,
             'score_threshold': score_threshold,
             'display_lincomb': False,
             'top_k': top_k,
             'eval_mask_branch': True,
             }
        self.args = SimpleNamespace(**args_dict)

    @staticmethod
    def get_model(weights_path, cuda):
        model = Yolact()
        map_location = None if cuda else torch.device('cpu')
        model.load_weights(weights_path, map_location=map_location)
        return model

    @torch.no_grad()
    def predict(self, img):
        preds = eval.evalimage(self.model, img)
        t = postprocess(preds, 1320, 512, visualize_lincomb=self.args.display_lincomb,
                        crop_masks=self.args.crop,
                        score_threshold=self.args.score_threshold)
        idx = t[1].argsort(0, descending=True)[:self.args.top_k]
        if args.eval_mask_branch:
            masks = t[3][idx]
        classes, scores, boxes = [x[idx].cpu().detach().numpy() for x in t[:3]]
        return InstanceSegmentationCoal(masks=np.array(masks))

if __name__ == '__main__':
    image = cv2.imread(str(EXAMPLE_IMG))
    yol_model = YolactPredictor(WEIGHTS_DIR / 'yolact_base_201_2013_interrupt.pth')
    coals = yol_model.predict(image)
    print([coal.get_fraction() for coal in coals])
    cv2.imshow('Contours', coals[0].plot_on(image))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
