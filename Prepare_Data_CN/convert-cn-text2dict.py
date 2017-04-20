# -*- coding: UTF-8 -*-
# python3
"""
字典结构
第一个元素是词;
第二个元素是index;
第三个元素是在全部数据集中出现的次数;
第四个元素是包含该元素的对话个数;

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

class ConvertCnText2Dict(object):
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
        word_counter = Counter()
        for line in open(self.args.input, 'r'):
            per_dialog = line.strip()
            if len(per_dialog) <= self.txt_max_length:
                try:
                    line_words = self.segment_call_api(per_dialog)
                    if len(line_words) > 1 :
                        if line_words[len(line_words) - 1]["word"] != self.end_of_utterance:
                            line_words.append({"word":self.end_of_utterance})
                        s = [x["word"] for x in line_words]
                        word_counter.update(s)
                except:
                    traceback.print_exc()
                    pass 
            else:
                pass
        total_freq = sum(word_counter.values())
        logger.info("字典中所有的词的次数是 %d " % total_freq)

        vocab_count = word_counter.most_common()
        vocab = {self.unk: 0, self.end_of_utterance: 1, self.end_of_dialog: 2, '<first_speaker>': 3, \
                 '<second_speaker>': 4, '<third_speaker>': 5, '<minor_speaker>': 6, \
                 '<voice_over>': 7, '<off_screen>': 8, '<pause>': 9}

        # Add other tokens to vocabulary in the order of their frequency 按词频排序
        i = 10
        for (word, count) in vocab_count:
            if not word in vocab:
                vocab[word] = i
                i += 1
        logger.info("Vocab size %d" % len(vocab))
        return vocab

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

    #################################
    # Part II: Binarize the dialogues
    #################################
    def binarize_dialog(self, vocab):
        # Everything is loaded into memory for the moment
        binarized_corpus = []
        # Some statistics
        unknowns = 0.
        num_terms = 0.
        freqs = collections.defaultdict(lambda: 0)
        # counts the number of dialogues each unique word exists in; also known as document frequency
        df = collections.defaultdict(lambda: 0)
        for line, dialogue in enumerate(open(self.args.input, 'r')):
            per_dialog = dialogue.strip()
            if len(per_dialog) <= self.txt_max_length:
                dialogue_words = self.segment_call_api(per_dialog)
                if len(dialogue_words) > 1:
                    if dialogue_words[len(dialogue_words) - 1]["word"] != self.end_of_utterance:
                        dialogue_words.append({"word":self.end_of_utterance})
            else:
                pass

            # Convert words to token ids and compute some statistics
            dialogue_word_ids = []
            for word in dialogue_words:
                word_id = vocab.get(word["word"], 0)
                dialogue_word_ids.append(word_id)
                unknowns += 1 * (word_id == 0)
                freqs[word_id] += 1

            num_terms += len(dialogue_words)

            # Compute document frequency statistics
            unique_word_indices = set(dialogue_word_ids)
            for word_id in unique_word_indices:
                df[word_id] += 1

            # Add dialogue to corpus
            if len(dialogue_word_ids)>0:
                binarized_corpus.append(dialogue_word_ids)

        self.safe_pickle(binarized_corpus, self.args.output + ".dialogues.pkl")
        self.safe_pickle([(word, word_id, freqs[word_id], df[word_id]) for word, word_id in vocab.items()],
                    self.args.output + ".dict.pkl")
        logger.info("Number of unknowns %d" % unknowns)
        logger.info("Number of terms %d" % num_terms)
        logger.info("Mean document length %f" % float(sum(map(len, binarized_corpus)) / len(binarized_corpus)))
        logger.info(
            "Writing training %d dialogues (%d left out)" % (len(binarized_corpus), line + 1 - len(binarized_corpus)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="一行是一个对话")
    parser.add_argument("output", type=str, help="输出目录")
    args = parser.parse_args()
    if not os.path.isfile(args.input):
        raise Exception("Input file not found!")
    convert = ConvertCnText2Dict(args)
    vocab = convert.gen_dialog_txt2words()
    time.sleep(5)
    convert.binarize_dialog(vocab)
