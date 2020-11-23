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
    
    def save_txt(self, path, data_list, mode='w', encoding='utf-8'):
        """
        @brief テキストデータにセーブする
        @param path (str) セーブするパス
        @param data_list (list) データリスト
        @param mode (str) 
        @param encoding (str) 
        """
        ret_is_save = True
        try:
            with open(path, mode=mode, encoding=encoding) as file:
                for data in data_list:
                    file.writelines(data+'\n')
        except Exception as e:
            print('[ERROR]{}'.format(e.args()))
            ret_is_save = False
        return ret_is_save
        
    def get_file_path_list(self, path, recursive=True, ext="png"):
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
            path = os.path.join('{}/**/*.{}'.format(path, ext))
        else:
            path = os.path.join('{}/*.{}'.format(path, ext))
        ret_list = glob.glob(path, recursive=recursive)
        return ret_list
    
    def get_dir_list(self, path):
        """
        @brief 指定パス直下にあるディレクトリ群を取得する
        @param path (str) 得たいディレクトリ群がある親フォルダのパス
        @returm ret_list (list) 取得したディレクトリパスリスト
        """
        ret_list = []
        path = os.path.join("{}/**/".format(path))
        dir_path_list = glob.glob(path, recursive=False)
        for dir_path in dir_path_list:
            dir_path_const = dir_path.split("/")
            new_dir_path = ("/").join(dir_path_const[:-1])
            ret_list.append(new_dir_path)
        return ret_list
