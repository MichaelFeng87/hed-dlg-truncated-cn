# -*- coding: UTF-8 -*-
#python3 
import word2vec
import argparse
import os
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="一行是一个对话")
    parser.add_argument("output", type=str, help="输出")
    args = parser.parse_args()
    if not os.path.isfile(args.input):
        raise Exception("Input file not found!")
    word2vec.word2vec(args.input, args.output, size=100,verbose=True)
