"""
@file classifier.py
@brief 画像ファイルを球団、選手名別に整理する。

@author Shunsuke Hishida / created on 2020/09/27
"""
import argparse
import os
import shutil

import cv2
import numpy as np

from config.crop_position import CropPosition
from manage.file_manager import FileManager
from preprocess.image import ImagePreprocess
from preprocess.interface import PreProcessInterface

class Classifier(object):
    """
    @brief 画像ファイルを球団、選手名別に整理する。
    """
    def __init__(self):
        """
        @brief コンストラクター
        """
        self.__cp = CropPosition()
        self.__fm = FileManager()
        self.__ip = ImagePreprocess()
        self.__pi = PreProcessInterface()

        team_flag_imgs_path = "/media/hishida/disk/000_dataset/team_flag_2020"
        self.__tf_path_list = [team_flag_path for team_flag_path in self.__fm.get_file_path_list(team_flag_imgs_path)]
        self.init_img_info()


    def init_img_info(self):
        """
        @brief img_info_listを初期化する
        """
        self.__img_info_list = []


    def debug_img(self, basename, img, ext="jpg"):
        path = os.path.join("/home/hishida/Desktop", basename+"."+ext)
        self.__fm.save_image(path, img)


    def estimate_team(self, player_img):
        """
        @brief ヒストグラムを算出し、チームを特定する。
        @param player_img (numpy.ndarray) 選手画像
        """
        hist_list = []
        target_img = self.__ip.crop(player_img, self.__cp.TEAM_FLAG)
        target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
        target_hist = cv2.calcHist([target_img], channels=[0], mask=None, histSize=[200], ranges=[0, 200])
        for tf_path in self.__tf_path_list:
            tf_img = self.__fm.load_image(tf_path)
            tf_img = cv2.cvtColor(tf_img, cv2.COLOR_BGR2GRAY)
            compare_hist = cv2.calcHist([tf_img], channels=[0], mask=None, histSize=[200], ranges=[0, 200])
            ret_hist = cv2.compareHist(target_hist, compare_hist, 0)
            hist_list.append(ret_hist)
        max_hist = max(hist_list)
        max_index = hist_list.index(max_hist)
        team_path = self.__tf_path_list[max_index]
        team_name, _ = os.path.splitext(os.path.basename(team_path))
        self.__img_info_list.append(team_name)


    def read_player_name(self, player_img, file_name, build_option_num=6, thresh_min=105):
        """
        @brief 画像から選手名を読み取る
        @param player_img (numpy.ndarray) 選手画像
        @param file_name (str) ファイル名
        @param build_option_num (int) pyocrのオプション番号
        """
        player_name = self.__pi.crop_img2word(player_img, self.__cp.PLAYER_NAME, file_name, build_option_num=10, thresh_min=thresh_min, gauss=True, padding=True)
        self.__img_info_list.append(player_name)


    def judge_page_num(self, player_img, file_name, build_option_num=6, thresh_min=200):
        """
        @brief ページ番号を決める
        @param player_img (numpy.ndarray) 選手画像
        @param file_name (str) ファイル名
        @param build_option_num (int) pyocrのオプション番号
        build_option_num is the same as function of read_player_name.
            0 = Orientation and script detection (OSD) only.
            1 = Automatic page segmentation with OSD.
            2 = Automatic page segmentation, but no OSD, or OCR
            3 = Fully automatic page segmentation, but no OSD. (Default)
            4 = Assume a single column of text of variable sizes.
            5 = Assume a single uniform block of vertically aligned text.
            6 = Assume a single uniform block of text.
            7 = Treat the image as a single text line.
            8 = Treat the image as a single word.
            9 = Treat the image as a single word in a circle.
            10 = Treat the image as a single character.
        """
        aptitude = self.__pi.crop_img2word(player_img, self.__cp.APTITUDE, file_name, build_option_num, thresh_min=thresh_min, gauss=True)
        main_aptitude = self.__pi.crop_img2word(player_img, self.__cp.MAIN_APTITUDE, file_name, build_option_num=8, thresh_min=180, padding=True, main_aptitude=True)
        chan_pin_usage = self.__pi.crop_img2word(player_img, self.__cp.CHAN_PIN_USAGE, file_name, build_option_num, thresh_min=thresh_min, gauss=True)
        print("[aptitude]: {}\n[main_aptitude]: {}\n[chan_pin_usage]: {}".format(aptitude, main_aptitude, chan_pin_usage))
        if aptitude == "適性":
            if main_aptitude == "先" or main_aptitude == "中" or main_aptitude == "抑":
                self.__img_info_list.insert(1, "pitcher")
                self.__img_info_list.append("1")
            else:
                self.__img_info_list.insert(1, "fielder")
                self.__img_info_list.append("2")
        else:
            if main_aptitude == "投":
                self.__img_info_list.insert(1, "pitcher")
                if chan_pin_usage == "チャンス":
                    self.__img_info_list.append("2")
                elif chan_pin_usage == "対ピンチ":
                    self.__img_info_list.append("1")
                elif chan_pin_usage == "起用法":
                    self.__img_info_list.append("3")
                else:
                    self.__img_info_list.append("4")
            else:
                self.__img_info_list.insert(1, "fielder")
                if chan_pin_usage == "チャンス":
                    self.__img_info_list.append("1")
                elif chan_pin_usage == "対ピンチ":
                    self.__img_info_list.append("2")  
                elif chan_pin_usage == "起用法":
                    self.__img_info_list.append("3")
                else:
                    self.__img_info_list.append("4")

    def read_img_info(self, img_path):
        """
        @brief 画像から情報を読み取る
        @param img_path (str) 画像パス
        """
        basename = os.path.basename(img_path)
        player_img = self.__fm.load_image(img_path)
        self.estimate_team(player_img)
        self.read_player_name(player_img, basename)
        self.judge_page_num(player_img, basename)
        print(self.__img_info_list)
        

    def save_img(self, output_path, player_img_path, ext='jpg'):
        """
        @brief self.__img_info_listに格納されている情報をもとに画像をsaveする。
        @param output_path (str) 分類後の画像を収めるパス
        @param player_img_path (str) 選手画像のパス
        """
        player_img = cv2.imread(player_img_path)
        save_dir = os.path.join(output_path, self.__img_info_list[0], self.__img_info_list[1],
                                self.__img_info_list[2])
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, "{}.{}".format(self.__img_info_list[3], ext))
        cv2.imwrite(save_path, player_img)
    
    def main(self, d_path, o_path):
        """
        @brief メイン関数
        @param d_path (str) データセットパス
        @param o_path (str) アウトプットパス
        """
        player_img_list = self.__fm.get_file_path_list(d_path)
        for player_img_path in player_img_list:
            self.init_img_info()
            self.read_img_info(player_img_path)
            self.save_img(output_path, player_img_path)
    
if __name__ == "__main__":
    print("[start]")
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", required=True,
                        metavar="/media/hishida/disk/PS4/SHARE/Screenshots/eBASEBALL_pawapuro2020",
                        help="Directory of dataset")
    parser.add_argument("-o", required=True,
                        metavar="/media/hishida/disk/000_dataset/plaer_ver",
                        help="Directory of dataset")
    args = parser.parse_args()

    dataset_path = args.d
    output_path = args.o

    clsf = Classifier()
    clsf.main(dataset_path, output_path)

