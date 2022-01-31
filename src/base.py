from pathlib import Path
from typing import Dict, Tuple

import cv2
import numpy as np
from numpy.typing import NDArray

import sys
FILE = Path(__file__).resolve()
ROOT = FILE.parent  # root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

class BasePredictor:

    def predict(self, img: NDArray):
        raise NotImplementedError()


class Coals:

    def __init__(self, rectangles):
        self.rectangles = rectangles

    def get_fraction(self) -> NDArray:
        raise NotImplementedError()


class InstanceSegmentationCoals(Coals):

    @staticmethod
    def diag(box):
        return np.linalg.norm(box[0] - box[2])

    @staticmethod
    def longest_side(box):
        return max(np.linalg.norm(box[0] - box[1]), np.linalg.norm(box[1] - box[2]))

    def get_fraction(self) -> NDArray:
        boxes = [np.int0(cv2.boxPoints(rect)) for rect in self.rectangles]
        return np.array([self.longest_side(box) for box in boxes])

