"""
@file confirm_file_number.py
@brief 各選手フォルダー内のファイルの数を確認する

@author Shunsuke Hishida / created on 2020/11/22
"""

import os

from manage.file_manager import FileManager

class ConfirmFileNumber(object):
    """
    @brief 各選手フォルダー内のファイルの数を確認する 
    """
    def __init__(self):
        """
        @brief コンストラクター
        """
        self.__fm = FileManager()
    
    def __len__(self, list_num):
        """
        @brief リストの数を返す
        @param list (list) 数を数えるリスト
        @return (int) リスト内の要素数
        """
        return len(list_num)

    def main(self, input_path, output_path, ext="png"):
        """
        @brief main関数 
        @param input_path (str) 画像インプットパス
        @param input_path (str) 画像アウトプットパス
        """
        strange_data = []
        team_dir = self.__fm.get_dir_list(input_path)
        for team_path in team_dir:
            position_dir = self.__fm.get_dir_list(team_path)
            for position_path in position_dir:
                player_dir = self.__fm.get_dir_list(position_path)
                for player_path in player_dir:
                    player_data_list = self.__fm.get_file_path_list(player_path)
                    list_num = self.__len__(player_data_list)
                    if list_num >= 5:
                        player_path_const = player_path.split("/")
                        print("{} の {} にファイル数5つ以上確認".format(player_path_const[-4], player_path_const[-2]))
                        strange_data.append(player_path)
                        continue
                    elif list_num < 4:
                        name_list = ["1", "2", "3", "4"]
                        for player_data in player_data_list:
                            basename, _ = os.path.splitext(os.path.basename(player_data))
                            name_list.remove(basename)
                        for name in name_list:
                            rest_name_path = player_path + "/" + name +  "." + ext
                            strange_data.append(rest_name_path)
                    else:
                        print("{} は4ファイル確認されました。".format(player_path))
        self.__fm.save_txt(output_path, strange_data)

if __name__ == "__main__":
    input_path = "/media/hishida/disk/000_dataset/update03"
    output_path = "/media/hishida/disk/000_dataset/update03/lack_list.txt"
    cfn = ConfirmFileNumber()
    cfn.main(input_path, output_path)