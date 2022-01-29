"""
VGG json -> instance segmentation masks
VGG: https://www.robots.ox.ac.uk/~vgg/software/via/via.html
"""

import json
import shutil
from pathlib import Path
from typing import Dict, Any, List, Tuple

import cv2
import numpy as np
from numpy.typing import NDArray

Polygon = Tuple[Tuple[int, int], ...]

def parse_points(region) -> Polygon:
    """
    Extract X and Y coordinates
    :param region: region from VGG json
    :return: list of points x, y coordinates
    """
    x_points = region["shape_attributes"]["all_points_x"]
    y_points = region["shape_attributes"]["all_points_y"]
    return tuple(zip(x_points, y_points))

def vgg2dict(vgg_json: Path) -> Dict[str, List[Polygon]]:
    """
    VGG json -> vgg2dict (you are here) -> dict2mask -> mask

    :param vgg_json: path to VGG json annotation file
    :return: keys are filenames, values are list of polygons
    """

    with open(vgg_json) as f:
        annotations: Dict[str, Any] = json.load(f)

    mask_dict = {}
    for image_annotation in annotations.values():
        file_name: str = image_annotation["filename"]
        if not image_annotation["regions"]:
            print(f'No masks: {file_name}')
        mask_dict[file_name] = []
        for region in image_annotation["regions"]:
            polygon = parse_points(region)
            mask_dict[file_name].append(polygon)
    return mask_dict

def dict2mask(image_name: str, mask_dict: Dict[str, List[Polygon]],
                   mask_width: int = 1320, mask_height: int = 512) -> NDArray:
    """
    VGG json -> vgg2dict -> dict2mask (you are here) -> mask

    :param image_name: name of annotated image
    :param mask_dict: dict from vgg2dict
    :param mask_width: dimensions should match those of ground truth image
    :param mask_height: dimensions should match those of ground truth image
    :return: mask with values in range (0, num objects), unique for object
    """

    mask: NDArray = np.zeros((mask_height, mask_width))
    for polygon_num, polygon in enumerate(mask_dict[image_name]):
        polygon = np.array(polygon, dtype=np.int32)
        cv2.fillPoly(mask, [polygon], color=polygon_num + 1)
    return mask

def save_vgg2mask(source_folder: Path, save_folder: Path, vgg_json: Path,
                  mask_width: int = 1320, mask_height: int = 512) -> None:
    """
    Save mask from VGG annotation json as png image

    :param source_folder: images source
    :param save_folder: create dataset in this folder
    :param vgg_json: to VGG json
    :param mask_width: dimensions should match those of ground truth image
    :param mask_height: dimensions should match those of ground truth image
    :return: None, but save mask with values in range (0, num objects), unique for object
    """

    image_folder: Path = save_folder / "images"
    mask_folder: Path = save_folder / "masks"

    if not save_folder.is_dir():
        save_folder.mkdir()
    if not image_folder.is_dir():
        image_folder.mkdir()
    if not mask_folder.is_dir():
        mask_folder.mkdir()

    with open(vgg_json) as f:
        annotations: Dict[str, Any] = json.load(f)

    for image_annotation in annotations.values():
        file_name: str = image_annotation["filename"]
        if not image_annotation["regions"]:
            print(f'No masks: {file_name}')
            continue

        shutil.copy(src=source_folder / file_name, dst=image_folder / file_name)
        mask: NDArray = np.zeros((mask_height, mask_width))
        for polygon_num, region in enumerate(image_annotation["regions"]):
            polygon = parse_points(region)
            polygon = np.array(polygon, dtype=np.int32)
            cv2.fillPoly(mask, [polygon], color=polygon_num + 1)

        mask_path = (mask_folder / f'mask_{file_name}').with_suffix('.png')
        cv2.imwrite(str(mask_path), mask)


if __name__ == '__main__':
    save_vgg2mask(
        source_folder=Path.cwd().parent / "few_data",
        save_folder=Path.cwd().parent / "few_data_processed",
        vgg_json=Path.cwd().parent / "few_data.json"
    )
