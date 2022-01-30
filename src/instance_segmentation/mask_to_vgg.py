import cv2
import json
import numpy as np
from pathlib import Path
from numpy.typing import NDArray
from typing import Union, Dict, Generator, List


def mask2contours(mask: NDArray) -> NDArray:
    contours, _ = cv2.findContours((mask * 255).astype('uint8'), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return np.array(contours).flatten()

def masks2polygons(masks: NDArray) -> Generator[List[int], None, None]:
    for mask in masks:
        contours = mask2contours(mask)
        if contours.shape[0] >= 6:
            yield contours.tolist()


def masks2vgg(names_and_masks: Dict[str, NDArray], save_path: Union[str, Path]) -> None:

    vgg_annotation = {}
    for name, masks in names_and_masks.items():
        size = masks.size
        image_annotation = {
            'filename': name,
            'size': size,
            'regions': [],
            'file_attributes': {}
        }

        for polygon in masks2polygons(masks):
            # all_points_x, all_points_y = polygon[::2], polygon[1::2]
            all_points_x, all_points_y = polygon[::12], polygon[1::12]   # monkey smoothing
            image_annotation['regions'].append({
                'shape_attributes': {
                    'name': 'polygon',
                    'all_points_x': all_points_x,
                    'all_points_y': all_points_y
                },
                'region_attributes': {}
            })

        vgg_annotation[name + str(size)] = image_annotation

    with open(save_path, 'w+', encoding='utf-8') as f:
        json.dump(vgg_annotation, f, separators=(',', ':'))
