"""
Instance Segmentation dataset
Based on Penn-Fudan dataset from https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html
"""
from pathlib import Path
from typing import List

import numpy as np
import torch
import torch.utils.data
from PIL import Image

from train.converters.vgg_to_mask import vgg2dict, dict2mask


class CoalFractionDataset(torch.utils.data.Dataset):
    def __init__(self, root, vgg_json, width, height, transforms=None):
        self.root = Path(root)
        self.transforms = transforms
        # load all image files, sorting them to
        # ensure that they are aligned
        self.images: List[Path] = sorted(list(self.root.glob('*')))
        self.masks = vgg2dict(vgg_json)
        self.size = {'width': width, 'height': height}

    def __getitem__(self, idx):
        # load images ad masks
        img = Image.open(self.images[idx]).convert("RGB")
        mask = dict2mask(image_name=self.images[idx].name,
                         mask_dict=self.masks,
                         mask_width=self.size['width'],
                         mask_height=self.size['height'])
        # note that we haven't converted the mask to RGB,
        # because each color corresponds to a different instance
        # with 0 being background

        # instances are encoded as different colors
        obj_ids = np.unique(mask)
        # first id is the background, so remove it
        obj_ids = obj_ids[1:]

        # split the color-encoded mask into a set
        # of binary masks
        masks = mask == obj_ids[:, None, None]

        # get bounding box coordinates for each mask
        num_objs = len(obj_ids)
        boxes = []
        for i in range(num_objs):
            pos = np.where(masks[i])
            xmin = np.min(pos[1])
            xmax = np.max(pos[1])
            ymin = np.min(pos[0])
            ymax = np.max(pos[0])
            boxes.append([xmin, ymin, xmax, ymax])

        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        # there is only one class
        labels = torch.ones((num_objs,), dtype=torch.int64)
        masks = torch.as_tensor(masks, dtype=torch.uint8)

        image_id = torch.tensor([idx])
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        # suppose all instances are not crowd
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64)

        target = {
            "boxes": boxes,
            "labels": labels,
            "masks": masks,
            "image_id": image_id,
            "area": area,
            "iscrowd": iscrowd
        }

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.images)
