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


class Coal:

    def get_fraction(self) -> NDArray:
        raise NotImplementedError()


class InstanceSegmentationCoal(Coal):

    def __init__(self, contour):
        self.contour = contour

    @staticmethod
    def diag(box):
        return np.linalg.norm(box[0] - box[2])

    @staticmethod
    def longest_side(box):
        return max(np.linalg.norm(box[0] - box[1]), np.linalg.norm(box[1] - box[2]))

    def get_fraction(self) -> float:
        box = cv2.boxPoints(self.contour)
        return self.longest_side(box)

