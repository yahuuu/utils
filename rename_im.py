# -*- coding:utf-8 -*-
import cv2
import numpy as np
import os,sys
from random import shuffle


def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return cv_img

def org(file_path):
    return cv2.imread(file_path, cv2.IMREAD_COLOR)


# f_p  = "/media/sda3/py_proj/class4_idcard_bankcard/class_idcard_bankcard/test_i/101001/98.jpg"
# print(cv_imread(f_p)) # 12,7,4
# print(org(f_p))

def check_name(fp):
    unrenamed_ls = list()
    for root, file, imgls in os.walk(fp):
        if not imgls: continue
        for im in imgls:
            im_pth = os.path.join(root, im)
            # print(im_pth)
            unrenamed_ls.append(im_pth)
    shuffle(unrenamed_ls)
    for id, im in enumerate(unrenamed_ls):
        # os.rename(im, os.path.dirname())
        _base, _name = os.path.split(im)
        _name = str(id)+"."+ _name.split(".")[-1]
        os.rename(im, "{}/{}".format(_base, _name))



check_name("/media/sda3/py_proj/class4_idcard_bankcard/class_idcard_bankcard/test_i")