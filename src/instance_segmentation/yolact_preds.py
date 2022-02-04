import sys
sys.path.insert(0, '/content/yolact')
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
# from dataset import CoalFractionDataset
from src.base import BasePredictor, InstanceSegmentationCoal

from constants import EXAMPLE_IMG, WEIGHTS_DIR
from src.base import BasePredictor, InstanceSegmentationCoal
from src.utils import get_device, get_contours

class YolactPredictor(BasePredictor):
    def __init__(self, weights_path, args):
        self.model = self.get_model(weights_path, args)
        self.args = args

    @staticmethod
    def get_model(weights_path, args):
        model = Yolact()
        map_location = None if args.cuda else torch.device('cpu')
        model.load_weights(args.trained_model, map_location=map_location)
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
        return InstanceSegmentationStone(masks=np.array(masks))

if __name__ == '__main__':
    args_dict = {'images': '/content/few_data:/content/output_images',
             'fast_nms': True,
             'cuda': False,
             'mask_proto_debug': False,
             'cross_class_nms': False,
             'video': None,
             'image': '/content/few_data/20210712_141048_857A_ACCC8EAF31F3_0.jpg',
             'trained_model': '/content/yolact_base_201_2013_interrupt.pth',
             'crop': False,
             'score_threshold': 0.05,
             'display_lincomb': False,
             'top_k': 15,
             'eval_mask_branch': True,
             }
    global args
    args = SimpleNamespace(**args_dict)
    eval.set_args(args)
    eval.get_args()

    image = str(EXAMPLE_IMG)
    yol_model = YolactPredictor(WEIGHTS_DIR / '....pth', args)
    coals = yol_model.predict(image)
    print([coal.get_fraction() for coal in coals])

    cv2.imshow('Contours', coals[0].plot_on(image))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
