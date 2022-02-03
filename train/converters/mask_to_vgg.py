"""
Convert mask [N x W x H] to vgg json annotation
"""

import json
from pathlib import Path
from typing import Union, Dict, Generator, List, Tuple

from numpy.typing import NDArray

from src.utils import get_contour


def masks2polygons(masks: NDArray) -> Generator[Tuple[List[int], List[int]], None, None]:
    for mask in masks:
        contour = get_contour(mask)
        if contour.shape[0] >= 6:
            x, y = contour.T
            x, y = x.flatten(), y.flatten()
            yield x.tolist(), y.tolist()


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

        for all_points_x, all_points_y in masks2polygons(masks):
            all_points_x, all_points_y = all_points_x[::8], all_points_y[::8]  # monkey smoothing
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
