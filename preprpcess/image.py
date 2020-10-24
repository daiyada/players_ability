"""
@file file_manager.py
@brief ファイルの整理等をまとめたスクリプト

@author Shunsuke Hishida / created on 2020/10/08
"""
import os
import sys
import shutil

import cv2
import numpy as np
from PIL import Image
import pyocr

class ImagePreprocess(object):
    """
    @brief  イメージファイルを加工するファイル
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
    
    def img2word(self, img_path, build_option_num, lang='jpn'):
        """
        @brief 画像に書かれている文面を返す
        @param img_path (str) 読み取る画像のパス
        @return word (str) 画像から読み取った文字
        """
        # rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.open(img_path)
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print("No OCR tool did not be found.")
            sys.exit(1)
        tool = tools[0]
        word = tool.image_to_string(
            img,
            lang=lang,
            builder=pyocr.builders.TextBuilder(tesseract_layout=build_option_num)
        )
        return word
    
    def crop_img2word(self, img, crop_pos, file_name, build_option_num, thresh_min=100, gauss=False, erosion=False):
        """
        @brief 画像を切り出し切り出し範囲から単語を読み取る
        @param img (numpy.ndarray) 切り出したい画像
        @param crop_pos (list) [x_min, y_min, x_max, y_max]
        @param file_name (str) ファイル名
        @return word (str) 画像から読み取った文字
        """
        img = self.crop(img, crop_pos)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if gauss:
            img_gray = cv2.GaussianBlur(img_gray, (1,1), 0)
        _, img_binary = cv2.threshold(img_gray, thresh_min, 255, cv2.THRESH_BINARY)
        if erosion:
            img_binary = cv2.bitwise_not(img_binary)
            img_binary = self.erosion(img_binary)
            cv2.imwrite("/home/hishida/Desktop/test_erosion.jpg", img_binary)
            img_binary = self.dilation(img_binary)
            cv2.imwrite("/home/hishida/Desktop/test_dilation.jpg", img_binary)
            img_binary = cv2.bitwise_not(img_binary)
        tmp_save_path_dir = "/home/hishida/Documents/100_pawapuro/players_ability/tmp"
        os.makedirs(tmp_save_path_dir, exist_ok=True)
        tmp_save_path = os.path.join(tmp_save_path_dir, file_name) 
        cv2.imwrite(tmp_save_path, img_binary)
        cv2.imwrite("/home/hishida/Desktop/test.jpg", img_binary)
        word = self.img2word(tmp_save_path, build_option_num)
        input()
        shutil.rmtree(tmp_save_path_dir)
        return word