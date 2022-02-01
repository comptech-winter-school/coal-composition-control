"""
Convert VGG json to rotation-yolov5 annotation
https://github.com/BossZard/rotation-yolov5
"""

import json
from typing import Union

import cv2
import numpy as np

from constants import *


def vgg_to_rotated_yolo(
        dataset_dir: Union[str, Path],
        vgg_path: Union[str, Path],
        outdir: Union[str, Path] = None,
):

    dataset_dir = Path(dataset_dir)
    vgg_path = Path(vgg_path)
    outdir = dataset_dir.parent / 'labels' if outdir is None else Path(outdir)
    if not outdir.is_dir():
        outdir.mkdir()

    with open(vgg_path) as f:
        vgg = json.load(f)

    for v in vgg.values():
        image_path = dataset_dir / v['filename']
        image = cv2.imread(str(image_path))
        height, width = image.shape[:2]

        annotations = ''
        for r in v["regions"]:
            x, y = r["shape_attributes"]["all_points_x"], r["shape_attributes"]["all_points_y"]
            ((xc, yc), (w, h), theta) = cv2.minAreaRect(np.array(list(zip(x, y))))
            xc, w = xc / width,  w / width
            yc, h = yc / height, h / height
            theta = max(0, theta)
            annotations += f'0 {xc} {yc} {w} {h} {theta}\n'
        with open(outdir / image_path.with_suffix('.txt').name, 'w+', encoding='utf-8') as f:
            f.write(annotations)


if __name__ == "__main__":

    vgg_to_rotated_yolo(
        dataset_dir=DATA_DIR / 'few_data',
        vgg_path=DATA_DIR / 'few_data.json',
        outdir=DATA_DIR / 'few_data_labels',
    )
