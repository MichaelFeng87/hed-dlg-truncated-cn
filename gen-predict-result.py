# -*- coding: utf-8 -*-
# python3
import pymysql
import traceback
import datetime
import requests
import json
import re
import argparse

# 从阿基米德topic和reply中抽取数据，形成对话
class Predict(object):
    def __init__(self):
        mode = "prod"
        if mode == 'prod':
            self.to_word_api = 'http://218.244.132.122:8080/api/HanLpAPI/toWord'
            self.source_mysql_host="rdsy67za3yvibvq.mysql.rds.aliyuncs.com"
            self.source_mysql_db="ajmide_main_m"
            self.source_mysql_user="ajmide_stat_read"
            self.source_mysql_passwd="vnhf762Hfg3"
            self.end_of_utterance = "<sss> "
            self.end_of_dialog = " <sss> <ddd> <sss> \n"
            self.first_speaker = "<first_speaker> "
            self.second_speaker = "<second_speaker> "
            self.unk = "<unk>"
            self.all_path = './predict_result.txt'

    def gen_predict(self, path_raw, path_predict ):
        file_raw = open(path_raw)
        file_predict = open(path_predict)
        try:
            num_raw = 0
            raw_data = {}
            for line in file_raw:
                num_raw = num_raw + 1
                #content = line.replace("\n","")
                content = line
                raw_data[num_raw] = content
        finally:
            file_raw.close()

        try:
            num_predict = 0
            predict_data = {}
            for line in file_predict:
                num_predict = num_predict + 1
    #            content = line.replace("\n","")
                content = line
                predict_data[num_predict] = content
        finally:
            file_predict.close()
        try:
            all_file_object = open(self.all_path, 'w')
            for key in raw_data.keys():
                all_file_object.writelines(raw_data[key])
                all_file_object.writelines(predict_data[key])
                all_file_object.writelines('\n')
        finally:
            all_file_object.close()
        print("Done!")            
 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path_raw", type=str, help="")
    parser.add_argument("path_predict", type=str, help="")
    args = parser.parse_args()
    c = Predict()
    path_raw = args.path_raw
    path_predict = args.path_predict
    c.gen_predict(path_raw, path_predict)
