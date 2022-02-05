from typing import List

import cv2
import numpy as np
from numpy.typing import NDArray


class Coal:

    def get_fraction(self) -> NDArray:
        raise NotImplementedError()

    def plot_on(self, img: NDArray, color=(0, 255, 0), thickness=2) -> NDArray:
        raise NotImplementedError()

class BasePredictor:

    def predict(self, img: NDArray) -> List[Coal]:
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
        box = cv2.minAreaRect(self.contour)
        box = cv2.boxPoints(box)
        return self.longest_side(box)

    def plot_on(self, img: NDArray, color=(0, 255, 0), thickness=2) -> NDArray:
        cv2.drawContours(image=img, contours=[self.contour],
                         contourIdx=-1, color=color, thickness=thickness, lineType=cv2.LINE_AA)
        return img

class DetectionCoal(Coal):

    def __init__(self, box: List[int]):
        # box= [xmin, ymin, xmax, ymax]
        self.box = box

    @staticmethod
    def longest_side(box):
        return max(box[2] - box[0], box[3] - box[1])

    def get_fraction(self) -> float:
        return self.longest_side(self.box)

    def plot_on(self, img: NDArray, color=(0, 255, 0), thickness=2) -> NDArray:
        xmin, ymin, xmax, ymax = self.box
        contour = [[xmax, ymax], [xmax, ymin], [xmin, ymin], [xmin, ymax]]
        contour = np.int0(np.array(contour))
        cv2.drawContours(image=img, contours=[contour],
                         contourIdx=-1, color=color, thickness=thickness, lineType=cv2.LINE_AA)
        return img
