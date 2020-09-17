# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
from bottleneck import partition, nansum, nanmax


# import bottleneck


##最好w > preh  ## w= 11 会比默认节省 7% 时间,    w= 35 会比默认 节省50% 时间   ##时间花销与 preh/w  成正比
##错误，不再能通过max 优化，如果第1列有最大值，则 max(max_tmp2,max_Mat[j+w_tmp])不准确
##如果用下标优化，if + argpartition 最后效果不好
##如果要进一步优化，试着考虑 向下获取时优化
def ui_imb_2_move_fast3(im, w=11, preh=6):
    w_tmp = (w - 1) // 2
    row0, col0 = im.shape

    im_n = np.zeros((row0 + 2 * w_tmp, col0 + 2 * w_tmp), np.int32)

    im_n[w_tmp:row0 + w_tmp - 1 + 1, w_tmp:w_tmp + col0 - 1 + 1] = im

    row, col = row0 + 2 * w_tmp, col0 + 2 * w_tmp

    imb_tmp = []

    for i in range(w_tmp, row - w_tmp):

        preh_Mat = -partition(-im_n[i - w_tmp:i + w_tmp + 1, 0:col], preh, axis=0)[:preh]
        #
        tmp_data = preh_Mat[:, 0:w_tmp + w_tmp + 1].T.ravel()

        tmp2 = -partition(-tmp_data, preh)[:preh]

        imb_tmp.append((nansum(tmp2) - nanmax(tmp2)) * 1.0 / (preh - 1))

        for j in range(w_tmp + 1, col - w_tmp):
            start_index = ((j - w_tmp - 1) % w) * preh  ##笔记本倒数几页有推导

            tmp_data[start_index:start_index + preh] = preh_Mat[:, j + w_tmp]

            tmp2 = -partition(-tmp_data, preh)[:preh]

            imb_tmp.append((nansum(tmp2) - nanmax(tmp2)) * 1.0 / (preh - 1))

    imb = np.round(imb_tmp).reshape(row0, col0)

    return np.uint8(imb)


def ui_imb_2_move(im, w=11, preh=6):  ##w一定要是奇数

    w_tmp = (w - 1) // 2
    row0, col0 = im.shape

    im_n = np.zeros((row0 + 2 * w_tmp, col0 + 2 * w_tmp), np.int32)
    #    im_n[w_tmp:row0+w_tmp-1+1,w_tmp:w_tmp+col0-1+1]=im.copy()
    im_n[w_tmp:row0 + w_tmp - 1 + 1, w_tmp:w_tmp + col0 - 1 + 1] = im

    row, col = row0 + 2 * w_tmp, col0 + 2 * w_tmp

    imb_tmp = []

    for i in range(w_tmp, row - w_tmp):

        tmp_data = im_n[i - w_tmp:i + w_tmp + 1, 0:w_tmp + w_tmp + 1].T.ravel()

        tmp2 = -partition(-tmp_data, preh)[:preh]

        imb_tmp.append((nansum(tmp2) - nanmax(tmp2)) * 1.0 / (preh - 1))

        for j in range(w_tmp + 1, col - w_tmp):
            start_index = ((j - w_tmp - 1) % w) * w
            #            tmp_data[start_index:start_index+w]=im_n[i-w_tmp:i+w_tmp+1,j+w_tmp].copy()
            tmp_data[start_index:start_index + w] = im_n[i - w_tmp:i + w_tmp + 1, j + w_tmp]

            tmp2 = -partition(-tmp_data, preh)[:preh]

            imb_tmp.append((nansum(tmp2) - nanmax(tmp2)) * 1.0 / (preh - 1))

    imb = np.round(imb_tmp).reshape(row0, col0)
    return np.uint8(imb)


def removeLight(img, w=11, preh=6):
    #    pattern=ui_imb_2_move(img,w=w,preh=preh)
    pattern = ui_imb_2_move_fast3(img, w=w, preh=preh)

    img32 = np.float32(img)
    pattern32 = np.float32(pattern) + 1e-3

    aux = 1 - (img32 / pattern32)

    # Scale it to convert to 8bit format
    aux = aux * 255
    aux[aux < 0] = 0
    aux = np.uint8(np.round(aux))
    return ~aux


##一定要把背景去掉，所以 img32 >= pattern32(背景更强时，返回255)
##重点在前景下去除背景,所以如果背景强则返回255
##函数removeLight不用 img32+1e-3 因为背景都是最大前1:preh，所以背景一般不为0
def removeLight_imbExisted(img, pattern):
    img32 = np.float32(img) + 1e-3
    pattern32 = np.float32(pattern) + 1e-6

    aux = 1 - (img32 / pattern32)

    # Scale it to convert to 8bit format
    aux = aux * 255
    aux[aux < 0] = 0
    aux = np.uint8(np.round(aux))

    return ~aux


if __name__ == '__main__':

    img_file = r'C:\Users\yahuu\Desktop\machine\org\20200220161545.png'
    save_path = img_file.split(".")[0] +"_bin." +img_file.split(".")[1]
    gray = cv2.imread(img_file, 0)
    print("-->")
    print(gray)

    result = removeLight(gray)

    _, binary = cv2.threshold(result, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imshow('bin', binary);
    cv2.waitKey(-1)
    cv2.imwrite(save_path, binary)
