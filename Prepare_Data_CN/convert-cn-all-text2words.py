# -*- coding: UTF-8 -*-
# python3
"""
把对话分词
@author Feng Wei
"""
import collections
import numpy
import operator
import os
import sys
import logging
# import cPickle
import pickle as cPickle
from collections import Counter
import argparse
import requests
import json
import traceback
import re
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('cn-text2dict')

class ConvertCnText2Words(object):
    def __init__(self,args):
        self.unk = "<unk>"
        self.end_of_utterance = "<sss>"
        self.end_of_dialog = "<ddd>"
        self.txt_max_length = 600
        self.to_word_api = 'http://218.244.132.122:8080/api/HanLpAPI/toWord'
        self.args = args

    def safe_pickle(self, obj, filename):
        if os.path.isfile(filename):
            logger.info("Overwriting %s." % filename)
        else:
            logger.info("Saving to %s." % filename)
        with open(filename, 'wb') as f:
            # cPickle.dump(obj, f, protocol=cPickle.HIGHEST_PROTOCOL)
            cPickle.dump(obj, f, protocol=2)

    ###############################
    # Part I: Create the dictionary
    ###############################
    # 将mysql中topic和reply的数据转为对话,并存入txt
    def gen_2dialog_from_mysql(self):
        pass

    # 将txt中对话转为词形式
    def gen_dialog_txt2words(self):
        dialog_str = ""
        for line in open(self.args.input, 'r'):
            per_dialog = line.replace(self.end_of_utterance,"").replace(self.end_of_dialog,"").replace(" ","").replace("<first_speaker>","").replace("<second_speaker>","").replace("<third_speaker>","").replace("\n","")
            if len(per_dialog) <= self.txt_max_length:
                try:
                    line_words = self.segment_call_api(per_dialog)
                    if len(line_words) > 1 :
                        s = [x["word"] for x in line_words]
                        word_str = " ".join(s) + '\n' 
                        dialog_str = dialog_str + word_str
                except:
                    traceback.print_exc()
                    pass 
            else:
                pass
        save_path = self.args.output
        f = open(save_path,'w') 
        f.write(dialog_str)
        f.close()

    # 调用分词接口
    def segment_call_api(self, per_dialog):
        dialog_line = {"text": per_dialog, "stop":"true"}
        try:
            dialog_info = requests.post(self.to_word_api,params=dialog_line)
            ### for python3
            regex = re.compile(r'\\(?![/u"])')
            dialog_words = json.loads(regex.sub(r"\\\\", dialog_info.content.decode("utf-8")))
            ### for python2.7
            # dialog_words = json.loads(dialog_info.content.decode("utf-8").encode("utf-8"))
        except:
            traceback.print_exc()
            dialog_words = []
            pass
        return dialog_words

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="一行是一个对话")
    parser.add_argument("output", type=str, help="输出目录")
    args = parser.parse_args()
    if not os.path.isfile(args.input):
        raise Exception("Input file not found!")
    convert = ConvertCnText2Words(args)
    convert.gen_dialog_txt2words()
    print("done!")
