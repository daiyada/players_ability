"""
@file image.py
@brief 画像の前処理を行う

@author Shunsuke Hishida / created on 2020/10/08
"""
import os
import sys

import cv2
import numpy as np

class ImagePreprocess(object):
    """
    @brief イメージファイルを加工するファイル
    """
    def __init__(self):
        """
        @brief コンストラクタ
        """
        pass

    def crop(self, img, crop_pos):
        """
        @brief 画像をクロップする
        @param img (numpy.ndarray) 切り出したい画像
        @param crop_pos (list) [x_min, y_min, x_max, y_max]
        """
        crop_img = np.copy(img)
        x_min = crop_pos[0]
        y_min = crop_pos[1]
        x_max = crop_pos[2]
        y_max = crop_pos[3]
        ret_img = crop_img[y_min:y_max, x_min:x_max, :]
        return ret_img
    
    def erosion(self, img, k_size=(3,3), iter=1):
        """
        @brief 画像の白い部分が小さくなる収縮処理
        """
        e_img = np.copy(img)
        kernel = np.ones(k_size, np.uint8)
        ret_img = cv2.erode(e_img, kernel, iter)
        return ret_img
    
    def dilation(self, img, k_size=(3,3), iter=1):
        """
        @brief 画像の白い部分を大きくする膨張処理
        """
        d_img = np.copy(img)
        kernel = np.ones(k_size, np.uint8)
        ret_img = cv2.dilate(d_img, kernel, iter)
        return ret_img

    def get_blank_image(self, width, height, color=(255,255,255)):
        """
        @brief  サイズを指定して単色の画像を返す
        @param width (int) 生成する画像の幅
        @param height (int) 生成する画像の高さ
        @param color (tuple) 色コード
        @return blank (numpy.ndarray) 単色画像
        """
        b, g, r = color
        blank = np.zeros((width, height, 3), np.float32)
        blank += [b,g,r]
        return blank
    
    def composite(self, background_img, foreground_img, composite_pos=(0,0)):
        """
        @brief 背景と前景画像を合成する
        @param background_img (numpy.ndarray) 背景画像
        @param foreground_img (numpy.ndarray) 前景画像
        @return ret_img (numpy.ndarray) 合成画像 
        """
        b_img = np.copy(background_img)
        f_img = np.copy(foreground_img)
        h, w = f_img.shape[:2]
        x_min, y_min = composite_pos
        x_max = x_min + w
        y_max = y_min + h
        b_img[y_min:y_max, x_min:x_max] = f_img
        ret_img = b_img
        return ret_img
    
    def square_padding(self, img, width=512, height=512, color=(255, 255, 255)):
        """
        @brief 指定した背景色で元画像をパディングして画像サイズを変える
        @param img (numpy.ndarray) パディングする画像
        @param color (tuple) パディングする色
        @return ret_img (numpy.ndarray) パディングした後の画像
        """
        padding_img = self.get_blank_image(width=width, height=height, color=color)
        img_h, img_w, _ = img.shape
        pos_x = int((width - img_w)/2)
        pos_y = int((height - img_h)/2)
        ret_img = self.composite(padding_img, img, composite_pos=(pos_x, pos_y))
        return ret_img