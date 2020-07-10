# coding:utf-8

import os
import shutil
import random

# C:/work_data_set/盛京银行_版面识别分类数据集/传服务器/用于版面识别训练\一般缴款
split_ratio1 = (0.6, 0.2, 0.2)
split_ratio2 = (0.7, 0.2, 0.1)

def split(path):
    for root, dirs, filenames in os.walk(path):
        if not filenames:
            for dir in dirs:
                os.makedirs(os.path.join(root+"_train", dir), exist_ok=True)
                os.makedirs(os.path.join(root+"_val",   dir), exist_ok=True)
                os.makedirs(os.path.join(root+"_test",  dir), exist_ok=True)
        # print(root, dirs , filenames)
        random.shuffle(filenames)
        for idx, filename in enumerate(filenames):
            if idx <=  len(filenames)*split_ratio1[0]:
                # print(root.split(os.sep))
                _root, _dir = os.path.split(root)
                shutil.copy(src=os.path.join(root, filename), dst=os.path.join(_root+"_train", _dir, filename))
            elif len(filenames)*(split_ratio1[0]+split_ratio1[1]) >= idx >  len(filenames)*split_ratio1[0]:
                _root, _dir = os.path.split(root)
                shutil.copy(src=os.path.join(root, filename), dst=os.path.join(_root+"_val", _dir, filename))
            else:
                _root, _dir = os.path.split(root)
                shutil.copy(src=os.path.join(root, filename), dst=os.path.join(_root+"_test", _dir, filename))
    print("Done!")


if __name__ == "__main__":
    split(path=r"C:/work_data_set/盛京银行_版面识别分类数据集/传服务器/用于版面识别训练")