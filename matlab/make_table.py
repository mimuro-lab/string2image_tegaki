import sys
import scipy.io as sio
from PIL import Image
import cv2, jaconv
import numpy as np

pathToMat = "emnist-byclass.mat"

MAX_TRAIN_NUM = 100  # 学習データのバランスをとるため、各文字が100個を超えないようにします
mat_contents = sio.loadmat(pathToMat)
training_chr = mat_contents['dataset'][0][0][0][0][0][1]
training_img = mat_contents['dataset'][0][0][0][0][0][0]
chr_cnt = {}

def cnv_chr(code):
    if code <= 9:
        #res = chr(code + 48)  # 0-9
        res = 'del'
    elif code <= 35:
        #res = chr(code + 55)  # A-Z
        res = 'del'
    else:
        asc = code - 36
        asc = 97 + asc
        res = chr(asc)# a-z (今回は小文字は対象外とします)
        res = jaconv.h2z(res,digit=True,ascii=True)
    return res

open("emnist-byclass_table.csv", mode="w", encoding="utf-8")

fp = open("emnist-byclass_table.csv", mode="a", encoding="utf-8")

for i in range(len(training_img)):
    character = cnv_chr(training_chr[i][0])
    if(character != "del"):
        fp.write(str(i)+","+character+","+"ok\n")