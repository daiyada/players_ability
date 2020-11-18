"""
@file file_manager.py
@brief ファイルの整理等をまとめたスクリプト

@author Shunsuke Hishida / created on 2020/09/27
"""
import glob
import os

import cv2

class FileManager(object):
    """
    @brief ファイルの整理等をまとめたスクリプト
    """
    def save_image(self, path, img):
        """
        @brief 画像ファイルを保存する
        @param path (str) 画像のパス
        @param img (numpy.ndarray) 画像データ
        @return ret_saved (bool)
        """
        ret_saved = True
        try:
            cv2.imwrite(path, img)
        except Exception as e:
            print('ERROR:{}'.format(e))
            ret_saved = False
        return ret_saved
    
    def load_image(self, path):
        """
        @brief 画像ファイルを保存する。
        @param path (str) 画像のパス
        @return img (numpy.ndarray)　ロードした画像ファイル
        """
        img = cv2.imread(path)
        return img
        
    def get_file_path_list(self, path, recursive=True):
        """
        @brief ファイル内の指定した拡張子のファイルをリストで返す
        @param path (str) 特定ファイルのパス
        @param ext (str) 取得したいファイルの拡張子
        @param recursive (bool) ファイルパスを再帰的に取得するか否か
        @return ret_list (list) 取得したファイルリスト
        """
        ret_list = []
        if not os.path.exists(path):
            print('[ERROR][FileManager][get_file_path_list] Not exists {}.'.format(path))
            return ret_list

        if recursive == True:
            path = os.path.join('{}/**/*'.format(path))
        else:
            path = os.path.join('{}/*'.format(path))
        ret_list = glob.glob(path, recursive=recursive)
        return ret_list
