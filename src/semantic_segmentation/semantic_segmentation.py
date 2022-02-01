import numpy as np
import cv2
import albumentations as albu
import torch

import segmentation_models_pytorch as smp
from src.base import BasePredictor
from constants import WEIGHTS_DIR, DATA_DIR


class SemanticSegmentation(BasePredictor):
    def __init__(self, weights, segm_th_mask: float = 0.7, segm_th_edge: float = 0.7):
        self.model = self.get_model(weights)
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.preprocessing_fn = smp.encoders.get_preprocessing_fn('efficientnet-b0', 'imagenet')

        self.segm_th_mask = segm_th_mask
        self.segm_th_edge = segm_th_edge

        self.mask = None
        self.edges = None
        self.bound_mask = None

    @staticmethod
    def get_model(weights):
        model = torch.load(weights)
        model.eval()
        return model

    def draw_bounding_box(self):
        contours, hierarchy = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        img_box = cv2.cvtColor(self.mask, cv2.COLOR_GRAY2BGR)

        for cnt in contours[1:]:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(img_box, [box], 0, (0, 255, 0), 2)
        self.bound_mask = img_box

    @torch.no_grad()
    def predict(self, img):
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = albu.Compose([albu.Lambda(image=self.preprocessing_fn)])(image=image)['image']
        image = image.transpose(2, 0, 1).astype('float32')

        x_tensor = torch.from_numpy(image).to(self.device).unsqueeze(0)
        pr_mask = self.model.predict(x_tensor).squeeze(0).cpu().numpy()
        pr_mask = pr_mask.transpose(1, 2, 0)

        pr_mask_norm = np.where(pr_mask[:, :, 1:2] > self.segm_th_mask, 255, 0)
        pr_mask_norm_edge = np.where(pr_mask[:, :, 0:1] > self.segm_th_edge, 255, 0)

        self.mask, self.edges = pr_mask_norm.astype(dtype=np.uint8), pr_mask_norm_edge.astype(dtype=np.uint8)

        self.draw_bounding_box()
        # can add if for bound box
        # output json for found boxes
        # for small thr 3 coal == 1 - but a lot of white space, can check black/white to understand count of coal
        # area checker for bound is different class
        return self.bound_mask


if __name__ == '__main__':
    def visualize(img_from_camera, pred):
        cv2.imshow("orig", img_from_camera)
        cv2.imshow("predicted bound", pred)
        mixed = np.where(pred > 240, cv2.addWeighted(img_from_camera, 0.4, pred, 0.6, 1.0), img_from_camera)
        cv2.imshow("mixed", mixed)

        cv2.waitKey(231823)


    model = SemanticSegmentation(WEIGHTS_DIR / 'best_model3.pth',
                                 segm_th_mask=0.8)

    img_from_camera = cv2.imread(str(DATA_DIR / 'example.png'))
    pred = model.predict(img_from_camera)

    # tmp function
    visualize(img_from_camera, pred)
