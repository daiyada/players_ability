"""
@file interface.py
@brief 画像の前処理を行う

@author Shunsuke Hishida / created on 2020/10/08
"""
import os
import shutil

import cv2

from preprocess.image import ImagePreprocess
from preprocess.word import WordPreprocess

class PreProcessInterface(object):
    """
    @brief Preprocessフォルダ内のファイルを組み合わせて処理する
    """
    def __init__(self):
        """
        @brief コンストラクタ
        """
        self.__ip = ImagePreprocess()
        self.__wp = WordPreprocess()

    def crop_img2word(self, img, crop_pos, file_name, build_option_num, thresh_min=100, gauss=False,\
                     erosion=False, padding=False, main_aptitude=False):
        """
        @brief 画像を切り出し切り出し範囲から単語を読み取る
        @param img (numpy.ndarray) 切り出したい画像
        @param crop_pos (list) [x_min, y_min, x_max, y_max]
        @param file_name (str) ファイル名
        @return word (str) 画像から読み取った文字
        """
        img = self.__ip.crop(img, crop_pos)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if gauss:
            img_gray = cv2.GaussianBlur(img_gray, (1,1), 0)
        _, img_binary = cv2.threshold(img_gray, thresh_min, 255, cv2.THRESH_BINARY)
        if erosion:
            img_binary = cv2.bitwise_not(img_binary)
            img_binary = self.__ip.erosion(img_binary)
            img_binary = self.__ip.dilation(img_binary)
            img_binary = cv2.bitwise_not(img_binary)
        tmp_save_path_dir = "/home/hishida/Documents/100_pawapuro/players_ability/tmp"
        os.makedirs(tmp_save_path_dir, exist_ok=True)
        tmp_save_path = os.path.join(tmp_save_path_dir, file_name) 
        cv2.imwrite(tmp_save_path, img_binary)
        word = self.__wp.word_detection(tmp_save_path, build_option_num, main_aptitude=main_aptitude)
        shutil.rmtree(tmp_save_path_dir)
        return word