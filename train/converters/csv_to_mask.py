import glob
import json
import os
import shutil

import cv2
import numpy as np
import pandas as pd
from skimage.draw import polygon


def csv_to_df():
    all_df = []
    csvs = glob.glob(DEFAULT_PATH + "*.csv")
    for csv in csvs:
        cdf = pd.read_csv(csv)
        cdf['filename'] = cdf['filename']
        all_df.append(cdf)
    df = pd.concat(all_df)
    df = df.reset_index()
    df['region_shape_attributes'] = df['region_shape_attributes'].apply(json.loads)
    df = df[(df['region_count'] > 0)]

    return df


def cut_original_images(df):
    areas = df.groupby(['filename'])['region_shape_attributes'].apply(list)
    names = df.groupby(['filename'])['filename'].apply(list)
    name = [item[0] for item in names]
    if not os.path.exists(DEFAULT_PATH + 'img_cut/'):
        os.makedirs(DEFAULT_PATH + 'img_cut/')
    for img_idx in range(0, len(areas)):
        image_name = name[img_idx]
        cut_img = cv2.imread(DEFAULT_PATH + image_name)[:, 40:]  # cut to 1280 % 32 == 0

        cv2.imwrite(DEFAULT_PATH + 'img_cut/' + image_name, cut_img)


def save_mask(df, is_cut=True):
    areas = df.groupby(['filename'])['region_shape_attributes'].apply(list)
    names = df.groupby(['filename'])['filename'].apply(list)
    name = [item[0] for item in names]
    indexes = df.groupby(['filename'])['index'].apply(list)

    numbers_of_classes = 3

    fit_type_center = 'none'  # ['rectangle', 'circle', 'none']
    thickness_center = 2
    color_center = (255, 0, 0)
    radius_center = 2

    color_mask = (0, 0, 255)
    color_polygon = (0, 255, 0)
    thickness_polygon = 2

    if is_cut:
        global_path = DEFAULT_PATH + 'mask_cut_' + str(numbers_of_classes) + "_class/"
        if not os.path.exists(global_path):
            os.makedirs(global_path)
    else:
        global_path = DEFAULT_PATH + 'mask_' + str(numbers_of_classes) + "_class/"
        if not os.path.exists(global_path):
            os.makedirs(global_path)

    for img_idx in range(0, len(areas)):  # specific image
        image_name = name[img_idx]
        index_list = indexes[img_idx]
        if numbers_of_classes > 1:
            mask = np.zeros((orig_img.shape[0], orig_img.shape[1], 3), dtype=np.uint8)
            mask = np.where(mask == (0, 0, 0), (255, 0, 0), mask)
        else:
            mask = np.zeros((orig_img.shape[0], orig_img.shape[1], 1), dtype=np.uint8)
        i = 1
        for index in index_list:
            poly = df.iloc[index]['region_shape_attributes']
            rr, cc = polygon(poly['all_points_y'], poly['all_points_x'])
            rr[rr > mask.shape[0] - 1] = mask.shape[0] - 1  # sometimes out of bounds
            cc[cc > mask.shape[1] - 1] = mask.shape[1] - 1

            if numbers_of_classes > 1:
                points = []
                for i in range(0, len(poly['all_points_y'])):
                    points.append([poly['all_points_x'][i], poly['all_points_y'][i]])
                if fit_type_center == 'none':
                    pass
                elif fit_type_center == 'circle' or len(points) < 5:
                    circle = cv2.minEnclosingCircle(np.asarray(points))
                    cv2.circle(mask,
                               (int(circle[0][0]), int(circle[0][1])),
                               radius=radius_center,
                               color=color_center,
                               thickness=thickness_center)
                elif fit_type_center == 'rectangle':
                    rect = cv2.minAreaRect(np.asarray(points))
                    cv2.circle(mask,
                               (int(rect[0][0]), int(rect[0][1])),
                               radius=radius_center,
                               color=color_center,
                               thickness=thickness_center)
                mask[rr, cc] = color_mask
                mask = cv2.polylines(mask, np.asarray([points]), True, color_polygon, thickness_polygon)
            else:
                mask[rr, cc] = 255

            i += 1
            if is_cut:
                cv2.imwrite(global_path + image_name[:-3] + "png", mask[:, 40:])
            else:
                cv2.imwrite(global_path + image_name[:-3] + "png", mask)
    return global_path


def split_to_folders(df, res_path, split_rate=0.2, split_images=False):
    names = df.groupby(['filename'])['filename'].apply(list)
    name = [item[0] for item in names]

    val_names = name[:int(split_rate * len(name))]
    test_names = name[:int(split_rate * len(name))]
    train_names = name[int(split_rate * len(name)):]
    if split_images:
        if not os.path.exists(DEFAULT_PATH + 'train/'):
            os.makedirs(DEFAULT_PATH + 'train/')
        if not os.path.exists(DEFAULT_PATH + 'test/'):
            os.makedirs(DEFAULT_PATH + 'test/')
        if not os.path.exists(DEFAULT_PATH + 'val/'):
            os.makedirs(DEFAULT_PATH + 'val/')
        # assume that we're copying cut images
        for name in val_names:
            shutil.copyfile(DEFAULT_PATH + 'img_cut/' + name, DEFAULT_PATH + 'val/' + name)
        for name in test_names:
            shutil.copyfile(DEFAULT_PATH + 'img_cut/' + name, DEFAULT_PATH + 'test/' + name)
        for name in train_names:
            shutil.copyfile(DEFAULT_PATH + 'img_cut/' + name, DEFAULT_PATH + 'train/' + name)

    if not os.path.exists(DEFAULT_PATH + 'trainannot/'):
        os.makedirs(DEFAULT_PATH + 'trainannot/')
    if not os.path.exists(DEFAULT_PATH + 'testannot/'):
        os.makedirs(DEFAULT_PATH + 'testannot/')
    if not os.path.exists(DEFAULT_PATH + 'valannot/'):
        os.makedirs(DEFAULT_PATH + 'valannot/')
    for name in val_names:
        shutil.copyfile(res_path + name[:-3] + 'png', DEFAULT_PATH + 'valannot/' + name[:-3] + 'png')
    for name in test_names:
        shutil.copyfile(res_path + name[:-3] + 'png', DEFAULT_PATH + 'testannot/' + name[:-3] + 'png')
    for name in train_names:
        shutil.copyfile(res_path + name[:-3] + 'png', DEFAULT_PATH + 'trainannot/' + name[:-3] + 'png')


if __name__ == '__main__':
    # Put all dataset images + csv file to default path and run main
    # Be sure that orig_img path exists
    DEFAULT_PATH = "E:/few_data/fg/"
    orig_img = cv2.imread(DEFAULT_PATH + "20210712_141048_857A_ACCC8EAF31F3_0.jpg")

    df = csv_to_df()
    cut_original_images(df)
    res_path = save_mask(df, is_cut=True)
    split_to_folders(df, res_path, split_images=True)
