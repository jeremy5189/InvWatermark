#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import random
from argparse import ArgumentParser

import cv2
import numpy


class InvisibleWaterMark:

    def __init__(self):
        self.seed = 1

    def encode(self, image, watermark, result):
        # img = cv2.imread(image)
        # wm = cv2.imread(watermark)

        # h, w = img.shape[0], img.shape[1]
        # wm_h, wm_w = wm.shape[0], wm.shape[1]

        # m, n = range(h/2), range(w)

        # #  產生亂數
        # random.seed(self.seed)
        # random.shuffle(m)
        # random.shuffle(n)

        # rwm = numpy.zeros(img.shape)
        # for i in range(h/2):
        #     for j in range(w):
        #         if m[i] < wm_h and n[j] < wm_w:
        #             try:
        #                 rwm[i][j] = wm[i][j]
        #                 rwm[h - i - 1][w - j - 1] = rwm[i][j]
        #             except:
        #                 pass

        # res = numpy.fft.fft2(img) + rwm * 5
        # _img = numpy.fft.ifft2(res)
        # img_wm = numpy.real(_img)

        # cv2.imwrite(result, img_wm, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        img = cv2.imread(image)
        img_f = numpy.fft.fft2(img)
        height, width, channel = numpy.shape(img)
        watermark = cv2.imread(watermark)
        wm_height, wm_width = watermark.shape[0], watermark.shape[1]
        x, y = range(height / 2), range(width)
        random.seed(height + width)
        random.shuffle(x)
        random.shuffle(y)
        tmp = numpy.zeros(img.shape)
        for i in range(height / 2):
            for j in range(width):
                if x[i] < wm_height and y[j] < wm_width:
                    tmp[i][j] = watermark[x[i]][y[j]]
                    tmp[height - 1 - i][width - 1 - j] = tmp[i][j]
        res_f = img_f + 2 * tmp
        res = numpy.fft.ifft2(res_f)
        res = numpy.real(res)
        cv2.imwrite(result, res, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    def decode(self, image, encode_image, result):
        # img = cv2.imread(image)
        # img_wm = cv2.imread(encode_image)

        # h, w = img.shape[0], img.shape[1]

        # img_f = numpy.fft.fft2(img)
        # img_wm_f = numpy.fft.fft2(img_wm)
        # watermark = numpy.real((img_f - img_wm_f) / 5)
        # wm = numpy.zeros(watermark.shape)
        # #  產生亂數
        # m, n = range(h/2), range(w)
        # random.seed(self.seed)
        # random.shuffle(m)
        # random.shuffle(n)

        # for i in range(h / 2):
        #     for j in range(w):
        #         wm[m[i]][n[j]] = watermark[i][j]

        # cv2.imwrite(result, wm, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        ori = cv2.imread(image)
        img = cv2.imread(encode_image)
        ori_f = numpy.fft.fft2(ori)
        img_f = numpy.fft.fft2(img)
        height, width = ori.shape[0], ori.shape[1]
        watermark = (ori_f - img_f) / 2
        watermark = numpy.real(watermark)
        res = numpy.zeros(watermark.shape)
        random.seed(height + width)
        x = range(height / 2)
        y = range(width)
        random.shuffle(x)
        random.shuffle(y)
        for i in range(height / 2):
            for j in range(width):
                res[x[i]][y[j]] = watermark[i][j]
        cv2.imwrite(result, res, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


def build_parser():
    parser = ArgumentParser()
    parser.add_argument('--ori', dest='ori', required=True)
    parser.add_argument('--im', dest='im', required=True)
    parser.add_argument('--res', dest='res', required=True)
    parser.add_argument('--cmd', dest='cmd', required=True)
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
    watermark = InvisibleWaterMark()
    if cmd == 'encode':
        watermark.encode(ori, im, res)
    elif cmd == 'decode':
        watermark.decode(ori, im, res)
    else:
        parser.error("cmd %s does not exist." % im)


if __name__ == "__main__":
    main()
