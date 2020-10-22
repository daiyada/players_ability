"""
@file crop_team_flag.py
@brief 指定画像から球団フラグを切り取る

@author Shunsuke Hishida / created on 2020/09/27
"""
import argparse
import os

import cv2
import numpy as np

from config.crop_position import CropPosition
from manage.file_manager import FileManager
from preprpcess.image import ImagePreprocess

class CropTeamFlag(object):
    """
    @brief 指定画像から球団フラグを切り取る
    """
    def __init__(self):
        """
        @brief コンストラクタ
        """
        # gimpで計測した値 [x_min, y_min, x_max, y_max]
        # self.__crop_pos = [648, 224, 732, 284]

        # 保存する球団フラグの名前
        self.__flag_name = "example"
        
        self.__fm = FileManager()
        self.__ip = ImagePreprocess()
        self.__cp = CropPosition()
        

    def main(self, img_path, output_path, ext="jpg"):
        """
        @brief main関数
        @param img_path (str) 切り取る画像のパス
        @param output_path (str)　切り取った画像の保存先
        @param ext (str) 保存する拡張子　デフォルトjpg
        """
        print("main関数")
        img = cv2.imread(img_path)
        cropped_img = self.__ip.crop(img, self.__cp.TEAM_FLAG)
        flag_image_name = self.__flag_name + "." +ext
        save_path = os.path.join(output_path, flag_image_name)
        print("save_path: ", save_path)
        self.__fm.save_image(save_path, cropped_img)


if __name__ == "__main__":
    print("[START]")
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", required=True,
                        metavar="/media/hishida/disk/PS4/SHARE/Screenshots/eBASEBALL_pawapuro2020/a.jpg",
                        help="image data")
    parser.add_argument("-o", required=True,
                        metavar="/media/hishida/disk/000_dataset/plaer_ver",
                        help="Directory of dataset")
    args = parser.parse_args()

    img_path = args.d
    output_path = args.o

    ctf = CropTeamFlag()
    ctf.main(img_path, output_path)