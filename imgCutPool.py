# coding:utf-8
# Code date: 20200820

import os
import cv2 as cv
# from multiprocessing.pool import ThreadPool
from multiprocessing import Pool

KERNELS = max(os.cpu_count() , 1)
# KERNELS = 4
# print(KERNELS)

# 93, 1255
#      410, 1454
def save_sub_img(abspth, hwhw=(1255,93, 1454,410)):
    print(abspth)
    img_np = cv.imread(abspth, cv.IMREAD_COLOR)
    img_np = img_np[hwhw[0]:hwhw[2], hwhw[1]:hwhw[3],:]
    path_ls = os.path.split(abspth)
    dir = os.path.join(os.path.dirname(path_ls[0])+"_new",
                       os.path.basename(path_ls[0]))
    new_path = os.path.join(dir, path_ls[1])
    cv.imwrite(new_path, img_np)


def solutions():
    # img_dir = "/home/ai/tmp"
    # pool = ThreadPool(processes=KERNELS)
    pool = Pool(processes=KERNELS)
    img_dir = r"C:\work_data_set\qinhuangdaoBank\t1"
    for root, dir, filenames in os.walk(img_dir):
        # mk new dir
        if filenames:
            _ls = os.path.split(root)
            os.makedirs(os.path.join(_ls[0]+"_new", _ls[1]),exist_ok=True)

        # print(root, dir, filenames)
        if not filenames:
            continue
        for filename in filenames:
            if not filename.endswith(("jpg","jpeg", "JPG", "JPEG")):
                continue
            abspth = os.path.join(root, filename)
            # save_sub_img(abspth)
            pool.apply_async(save_sub_img, args=(abspth,))

        # pool.terminate()  # terminate 放在 join()之前，否报错
    pool.close()
    pool.join()


if __name__ == "__main__":
    import time
    t1 = time.time()
    solutions()
    print(time.time()-t1)
