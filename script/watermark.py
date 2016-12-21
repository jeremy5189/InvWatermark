#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import random
from argparse import ArgumentParser

import cv2
import numpy


class InvisibleWaterMark:

    def __init__(self, seed):
        self.seed = seed

    def encode(self, image, watermark, result):
        img = cv2.imread(image)
        watermark = cv2.imread(watermark)
        height, width = img.shape[0], img.shape[1]
        wm_h, wm_w = watermark.shape[0], watermark.shape[1]
        m, n = range(height/2), range(width)

        watermark_random = numpy.zeros(img.shape)

        #  使用亂數種子產生亂數
        random.seed(self.seed)

        #  將m跟n兩個陣列 洗牌
        random.shuffle(m)
        random.shuffle(n)

        #  將浮水印的圖片依據亂數種子產生新的頻率圖片
        for i in range(height/2):
            for j in range(width):
                if m[i] < wm_h and n[j] < wm_w:
                    watermark_random[i][j] = watermark[m[i]][n[j]]
                    watermark_random[height - i - 1][width - j - 1] = watermark_random[i][j]

        #  進行二維快速傅立葉轉換，將圖案變成頻率
        img_f = numpy.fft.fft2(img)

        # 將頻率圖案 加上 浮水印雜訊 並且放大倍數
        res = img_f + watermark_random * 1.5

        # 將傅立葉頻率 轉換為圖片
        img_wm = numpy.real(numpy.fft.ifft2(res))

        #  寫入檔案
        cv2.imwrite(result, img_wm, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    def decode(self, image, encode_image, result):
        img = cv2.imread(image)
        img_wm = cv2.imread(encode_image)

        h, w, c = img.shape[0], img.shape[1], img.shape[2]
        wm_h, wm_w, wm_c = img_wm.shape[0], img_wm.shape[1], img_wm.shape[2]

        #  如果圖片大小不一致，則將圖片複製補全，只能夠抵擋下方以及右方被裁切的攻擊。
        if wm_h != h or wm_w != w:
            new_img = numpy.zeros((h, w, c))
            for i in range(h):
                for j in range(w):
                    new_img[i][j] = img_wm[i % wm_h][j % wm_w]
            img_wm = new_img
        # 將原始圖片 以及 浮水印圖片 進行傅立葉轉換，並且相減取得頻率，之後放大頻率
        img_f = numpy.fft.fft2(img)
        img_wm_f = numpy.fft.fft2(img_wm)
        watermark = numpy.real((img_f - img_wm_f) * 5)
        wm = numpy.zeros(watermark.shape)

        #  依照之前產生的亂數種子解密
        m, n = range(h/2), range(w)
        random.seed(self.seed)
        random.shuffle(m)
        random.shuffle(n)

        #  依照相同亂數解出正確的圖片
        for i in range(h / 2):
            for j in range(w):
                wm[m[i]][n[j]] = watermark[i][j]
        for i in range(int(h / 2)):
            for j in range(w):
                wm[h-i-1][w-j-1] = wm[i][j]

        cv2.imwrite(result, wm, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


def build_parser():
    parser = ArgumentParser()
    parser.add_argument('--ori', dest='ori', required=True)
    parser.add_argument('--im', dest='im', required=True)
    parser.add_argument('--res', dest='res', required=True)
    parser.add_argument('--cmd', dest='cmd', required=True)
    parser.add_argument('--seed', dest='seed', required=False, default=100)
    return parser


def main():
    parser = build_parser()
    options = parser.parse_args()
    ori = options.ori
    im = options.im
    res = options.res
    cmd = options.cmd
    if not os.path.isfile(ori):
        parser.error("image %s does not exist." % ori)
    if not os.path.isfile(im):
        parser.error("image %s does not exist." % im)

    watermark = InvisibleWaterMark(options.seed)

    if cmd == 'encode':
        watermark.encode(ori, im, res)
    elif cmd == 'decode':
        watermark.decode(ori, im, res)
    else:
        parser.error("cmd %s does not exist." % im)


if __name__ == "__main__":
    main()
