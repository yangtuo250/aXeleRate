#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import cv2

WIDERPERSON_IMAGES_PATH = "/home/liuyk/data/WiderPerson/Images"
WIDERPERSON_ANNOTATIONS_PATH = "/home/liuyk/data/WiderPerson/Annotations"
YOLO_PATH = "/home/liuyk/data/WiderPerson/yolo"
LABEL_KEEP = [1, 2, 3]
SMALL_OBJECT_THRETH = 75 / 1024 # WilderPerson regard person height < 75 as small object in 1024 * 2048 image


def WiderPerson_to_yolo(img_file, ann_file, dest_ann_file):
    img = cv2.imread(os.path.join(WIDERPERSON_IMAGES_PATH, img_file))
    try:
        img_h, img_w = img.shape[:2]
    except AttributeError as e:
        print(os.path.join(WIDERPERSON_IMAGES_PATH, img_file), e)
        return
    # print(img_file, img_w, img_h)

    with open(os.path.join(WIDERPERSON_ANNOTATIONS_PATH, ann_file)) as fin:
        anns = fin.readlines()[1:]

    fout = open(os.path.join(YOLO_PATH, dest_ann_file), 'w')
    for ann in anns:
        ann_items = ann.split()
        label, xmin, ymin, xmax, ymax = [int(item) for item in ann_items]
        if label in LABEL_KEEP:
            x = (xmin + xmax) / 2 / img_w
            y = (ymin + ymax) / 2 / img_h
            w = (xmax - xmin) / img_w
            h = (ymax - ymin) / img_h
            if w < SMALL_OBJECT_THRETH or h < SMALL_OBJECT_THRETH:
                continue
            assert (x < 1 and x > 0 and y < 1 and y > 0 and w < 1 and w > 0 and h < 1
                    and h > 0), "Invalid annotation in %s, (%.2f, %.2f, %.2f, %.2f)" % (ann_file, x, y, w, h)
            fout.write(' '.join([str(0), str(x), str(y), str(w), str(h)]) + os.linesep)
    fout.close()

    return


def get_file_names(img_file_path):
    img_file = img_file_path.split(os.sep)[-1]
    ann_file = img_file + ".txt"
    dest_ann_file = img_file.replace(".jpg", ".txt")

    return img_file, ann_file, dest_ann_file


if __name__ == '__main__':
    assert len(sys.argv) == 2, "Usage: $0 img_file_path"
    img_file_path = sys.argv[1]
    img_file, ann_file, dest_ann_file = get_file_names(img_file_path)
    WiderPerson_to_yolo(img_file, ann_file, dest_ann_file)
