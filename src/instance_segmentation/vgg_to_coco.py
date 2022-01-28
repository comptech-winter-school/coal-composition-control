"""
Convert VGG json to COCO json, based on
https://stackoverflow.com/questions/61210420/converting-the-annotations-to-coco-format-from-mask-rcnn-dataset-format
"""
import math
from itertools import chain
import numpy as np
import json
import cv2
from pathlib import Path
from typing import Union


def poly_area(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

def vgg_to_coco(dataset_dir: Union[str, Path],
                vgg_path: Union[str, Path],
                outfile: Union[str, Path] = None,
                class_keyword: str = "label"):

    dataset_dir = Path(dataset_dir)
    vgg_path = Path(vgg_path)
    outfile = vgg_path.parent / f'coco_{vgg_path.name}' if outfile is None else Path(outfile)

    with open(vgg_path) as f:
        vgg = json.load(f)

    images_ids_dict = {}
    images_info = []
    for i,v in enumerate(vgg.values()):

        images_ids_dict[v["filename"]] = i
        image_path = dataset_dir / v['filename']
        image = cv2.imread(str(image_path))
        height, width = image.shape[:2]
        images_info.append({"file_name": v["filename"], "id": i, "width": width, "height": height})

    classes = {'coal'}
    category_ids_dict = {c: i for i, c in enumerate(classes, 1)}
    categories = [{"supercategory": class_keyword, "id": v, "name": k} for k, v in category_ids_dict.items()]
    annotations = []
    suffix_zeros = math.ceil(math.log10(len(vgg)))
    for i, v in enumerate(vgg.values()):
        for j, r in enumerate(v["regions"]):
            x, y = r["shape_attributes"]["all_points_x"], r["shape_attributes"]["all_points_y"]
            annotations.append({
                "segmentation": [list(chain.from_iterable(zip(x, y)))],
                "area": poly_area(x, y),
                "bbox": [min(x), min(y), max(x)-min(x), max(y)-min(y)],
                "image_id": images_ids_dict[v["filename"]],
                "category_id": 1,
                "id": int(f"{i:0>{suffix_zeros}}{j:0>{suffix_zeros}}"),
                "iscrowd": 0
                })

    coco = {
        "images": images_info,
        "categories": categories,
        "annotations": annotations
    }
    with open(outfile, "w") as f:
        json.dump(coco, f)


vgg_to_coco(dataset_dir=Path.cwd().parents[1] / 'few_data', vgg_path=Path.cwd().parents[1] / 'few_data.json')
