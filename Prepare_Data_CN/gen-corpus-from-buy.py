# -*- coding: utf-8 -*-
# python3
import pymysql
import traceback
import datetime
import requests
import json
import re

# 从阿基米德topic和reply中抽取数据，形成对话
class MatchTopicReply(object):
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
            self.all_path = './raw_data/buy_all.txt'
            self.train_path = './raw_data/buy_train.txt'
            self.valid_path = './raw_data/buy_valid.txt'
            self.test_path = './raw_data/all_test.txt'

    def gen_dialog(self, path):
        file_object = open(path)
        pattern= r"\[.*\]"
        p = re.compile(pattern)
        line_num = 0
        dialog_num = 0
        dialog = {}

        try:
            for line in file_object:
                line_num = line_num + 1
                content = line.replace("\n","")
                if len(content) != 0:
                    content_no_emoj = p.sub('', content)
                    if dialog_num in dialog.keys():
                        dialog[dialog_num].append(content_no_emoj)
                    else:
                        dialog[dialog_num]=[content_no_emoj]
                else:
                    dialog_num = dialog_num + 1 
        finally:
            file_object.close()

        try:
            all_file_object = open(self.all_path, 'w')
            for key in dialog.keys():
                speaker_1 = dialog[key][0]
                speaker_2 = dialog[key][1]
                dialog_context = self.end_of_utterance + self.first_speaker + speaker_1.replace("\n","") + self.end_of_utterance + self.second_speaker + speaker_2.replace("\n", "") + self.end_of_dialog
                all_file_object.writelines(dialog_context)
        finally:
            all_file_object.close()
        print("Done!")            
 
    def fetch_topic_reply_info(self):
        conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user, passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        topic_sql = "select topic_id, user_id, program_id, content, post_time from topic where mark_delete=0 and length(content) >0  and length(content)<800 order by post_time desc limit 2000"
        reply_sql = "select topic_id, reply_id, user_id, reply, post_time from reply where mark_delete=0 and length(reply)>0 order by post_time desc limit 100000"
        topic_dict = {}
        reply_dict = {}
        try:
            cursor.execute(topic_sql)
            topic_res = cursor.fetchall()
            for item in topic_res:
                topic_id = item["topic_id"]
                topic_content = item["content"]
                topic_dict[topic_id]=topic_content
            print("topic_dict: ", len(topic_dict))
            cursor.close()

            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(reply_sql)
            reply_res = cursor.fetchall()
            print("reply_res: ", len(reply_res))
            for item in reply_res:
                topic_id = item["topic_id"]
                reply = item["reply"]
                if topic_id not in reply_dict.keys():
                    reply_dict[topic_id]= [reply]
                else:
                    reply_dict[topic_id].append(reply)
            print("fetch done!!!")
            cursor.close()

            train_file_object = open(self.train_path, 'w') 
            valid_file_object = open(self.valid_path, 'w') 
            test_file_object = open(self.test_path, 'w') 
            for topic_id in topic_dict.keys():
                topic = topic_dict[topic_id]
                if topic_id in reply_dict.keys():
                    for reply in reply_dict[topic_id]:
                        dialog = self.end_of_utterance + self.first_speaker + topic.replace("\n"," ") + self.end_of_utterance + self.second_speaker + reply.replace("\n", " ") + self.end_of_dialog 
                        train_file_object.writelines(dialog)
                else:
                    dialog = self.end_of_utterance + self.first_speaker + topic.replace("\n", " ") + self.end_of_dialog 
                    test_file_object.writelines(dialog)
                    pass   
            train_file_object.close()
            valid_file_object.close()
            test_file_object.close()
        except:
            traceback.print_exc()
            pass
        print("数据准备完成!")
        cursor.close()
        conn.close()


if __name__ == '__main__':
    c = MatchTopicReply()
    path = './raw_data/buy_raw.txt'
    c.gen_dialog(path)
