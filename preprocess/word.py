"""
@word.py
@brief 文字認識の処理を行う

@author Shunsuke Hishida / created on 2020/10/08
"""
import os
import io
import re
import sys

from google.cloud import vision
from google.cloud.vision import types
import numpy as np
from PIL import Image
import pyocr

class WordPreprocess(object):
    """
    @brief 文字認識の前処理を行うクラス
    """
    def __init__(self):
        """
        @brief コンストラクタ
        """
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/hishida/Documents/100_pawapuro/key/daiyada07l6-ed7bded5bd2a.json"
    
    def word_detection(self, img_path, build_option_num, main_aptitude=False, lang="jpn"):
        """
        @brief 画像に書かれている文面を返す(Google Cloud Vision API)
        @param img_path (str) 読み取る画像のパス
        @return word (str) 画像から読み取った文字
        @return box (list) 文字のbboxリスト
        """
        client = vision.ImageAnnotatorClient()
        with io.open(img_path, "rb") as image_file:
            content = image_file.read()
        google_img = types.Image(content=content)
        response = client.text_detection(image=google_img)
        if not len(response.text_annotations):
            print("Google Cloud Vision APIでは読めませんでした。")
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
        else:
            word = response.text_annotations[0].description
        word = self.post_processing(word, main_aptitude=main_aptitude)
        return word
    
    def post_processing(self, word, main_aptitude=False):
        """
        @brief 解読した言葉の記号等を削除する
        @param word (str) 解読した文字列
        @return ret_word (str) 余分な部分を削除した文字列
        """
        ret_word = re.sub(r'[!-~]', "", word)
        ret_word = re.sub(r'[︰-＠]', "", word)
        ret_word = re.sub('\n', "", word)
        ret_word = ret_word.replace(" ", "")
        ret_word = ret_word.replace("　", "")
        ret_word = ret_word.replace("「", "")
        ret_word = ret_word.replace("『", "")
        if main_aptitude and len(ret_word) >= 2:
            print('通過')
            ret_word = ret_word[:-1]
        return ret_word