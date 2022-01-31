from pathlib import Path

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

    def plot_on(self, img: NDArray) -> NDArray:
        raise NotImplementedError()


class InstanceSegmentationCoal(Coal):

    def __init__(self, contours):
        self.contours = contours

    @staticmethod
    def diag(box):
        return np.linalg.norm(box[0] - box[2])

    @staticmethod
    def longest_side(box):
        return max(np.linalg.norm(box[0] - box[1]), np.linalg.norm(box[1] - box[2]))

    def get_fraction(self) -> float:
        box = cv2.minAreaRect(self.contours)
        box = cv2.boxPoints(box)
        return self.longest_side(box)

    def plot_on(self, img: NDArray) -> NDArray:
        cv2.drawContours(image=img, contours=[self.contours],
                         contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
        return img

