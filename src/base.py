from typing import Dict, Tuple

import cv2
import numpy as np
from numpy.typing import NDArray


class BasePredictor:

    def predict(self, img: NDArray):
        raise NotImplementedError()


class Coals:

    @staticmethod
    def get_size_map() -> Dict[str, Tuple[int, int]]:
        # with open(path) as f:
        #     size_map = json.load(f)
        size_map = {'s': (100, 199), 'm': (200, 299), 'l': (299, np.inf)}
        return size_map

    def get_fraction(self):
        raise NotImplementedError()


class InstanceSegmentationCoals(Coals):

    def __init__(self, masks):
        self.rectangles = [self.rectangle(mask) for mask in masks]
        self.size_map = self.get_size_map()

    @staticmethod
    def rectangle(mask):
        contours, _ = cv2.findContours((mask * 255).astype('uint8'), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return cv2.minAreaRect(contours[0])

    @staticmethod
    def diag(box):
        return np.linalg.norm(box[0] - box[2])

    @staticmethod
    def longest_side(box):
        return max(np.linalg.norm(box[0] - box[1]), np.linalg.norm(box[1] - box[2]))

    def get_fraction(self):
        boxes = [np.int0(cv2.boxPoints(rect)) for rect in self.rectangles]
        diagonal = np.array([self.longest_side(box) for box in boxes])
        fractions = {
            cat: np.count_nonzero((size[0] < diagonal) & (diagonal < size[1]))
            for cat, size in self.size_map.items()
        }
        return fractions

