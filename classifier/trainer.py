#!/usr/bin/python
# -*- coding:utf-8 -*-

import jieba
import os, sys
import math
import json
import word_is_num

path_file = os.path.abspath(sys.argv[0])
path_spider = os.path.abspath(os.path.join(path_file, os.pardir))
path_file = os.path.dirname(path_file) + '/'
path_spider = os.path.dirname(path_spider) + '/spider_json/'
print path_file
print path_spider

## 参数说明
 # all_frequency       array   所有训练集的单词数量的数组
 #     （形如 [232,121,...]，数组中两个为一对，分别对应一种类别重复的所有单词数，不重复的所有单词数）
 # all_word            array   所有训练集的单词
 #     （形如 ['computer', 'artificial',...]，每个代表一个训练集中的单词）
 # path_file           string  文本地址路径
all_frequency = []
all_word = []
kinds = 8

# 处理样本文档，获取样本文档的词频表，词频和
# 并把单词计入总训练集的单词all_word中
def getWordFre(index):
    # text_frequency      int     该类别的所有单词的词频和（即去除停用词后单词数量）
    # text_word_dic           object  该类别的词频表
    #     （形如 {'trainer': 23, 'classifier': 43, ...}）
    text_frequency = 0
    text_word_dic = {}

    # 得到语料中的样本文档，获得 index对应类别的 text_word_dic
    path_index = path_spider + 'data_' + str(index) + '.json'
    file_index = open(path_index, 'r')
    text_json = json.load(file_index)

    text_list = text_json['data']
    file_index.close()

    # for i in xrange(1, len(text_list)):
    i = 0
    for item in text_list:
        text = item['abstract']
        i += 1
        # path_index          string  该类别的文本的路径
        if (i % 20) == 0:      # 每处理100个文件 在控制台打印出对应的信息
            print str(i) + ' files have been trained.'

        # 对读取的文本进行分词
        # word_list           object  对text分词后的词对象
        word_list = jieba.cut(text, cut_all = False)
        # word_list = text

        # 获得停用词表
        file_stop = open(path_file + 'data/stop.txt')
        stop_word_list = file_stop.readlines()
        for j in xrange(0, len(stop_word_list)):
            stop_word = stop_word_list[j].strip()
            stop_word_list[j] = stop_word

        # 遍历每个样本文档的单词，若不是停用词则记录（包括样本文档的词频和，样本文档的词频表，以及总训练集）
        for word in word_list:
            word = word.lower().strip().encode('utf-8')

            if word_is_num.is_number(word) or word in stop_word_list:
                pass
            else:
                text_frequency = text_frequency + 1
                if word in text_word_dic:    #判断word是否统计过，如果在本文档中已经出现过，该词词频+1
                    text_word_dic[word] = text_word_dic[word] + 1
                else:
                    text_word_dic[word] = 1
                    if word not in all_word:
                        all_word.append(word)
    print 'There are ' + str(text_json['num']) + ' files in the ' + str(index) + ' kind.'
    return text_word_dic, text_frequency


# 通过getWordDic() 获得样本文档的词频和，词频表
# 把样本文档的词数，词频和记录到all_frequency 所有训练集的单词数组中
def WriteFreFile(index):
    (text_word_dic, text_frequency) = getWordFre(index)
    text_word_dic_num = len(text_word_dic)

    # 把样本文档的词数，词频和记录到all_frequency 所有训练集的单词数组中
    print 'num = ' + str(text_word_dic_num) + ', fre = ' + str(text_frequency) + '\n'
    all_frequency.append(str(text_word_dic_num))
    all_frequency.append(str(text_frequency))

    word_list = sorted(text_word_dic.iteritems(), key=lambda asd: asd[1], reverse=True)
    path_index_fre = 'word_fre/index_fre/' + str(index) + '_fre.txt'
    file_index_fre = open(path_index_fre, 'w')

    # 保存每一个训练文本的单词集合（每个单词 以及 它出现的次数）
    for word_fre in word_list:
        file_index_fre.write(word_fre[0] + ',' + str(word_fre[1]) + '\n')
    file_index_fre.close


# 这是训练前的预处理函数
# 作用是计算出每个类别的样本文档词频和，词频表，以供训练用
def prepare():
    for index in xrange(1, kinds+1):
        WriteFreFile(index)

    # 在all_word_num.txt文件中记录训练的单词总数，以及每一个类别样本文档的（所有单词数，不重复单词数）
    file_all_word = open('word_fre/all_word_num.txt', 'w')
    all_word_num = len(all_word)
    file_all_word.write(str(all_word_num) + '\n')
    print all_frequency
    for i in xrange(0, kinds*2-1, 2):
        file_all_word.write(all_frequency[i] + ',' + all_frequency[i + 1] + '\n')
    file_all_word.close


# 训练的主体函数
# 计算对应index的类别的样本文档中 每个单词对应的 P值
def training(index):
    print 'training : ' + str(index)
    path_all_word = 'word_fre/all_word_num.txt'
    file_all_word = open(path_all_word, 'r')

    # all_word_num.txt中的单词总数（所有单词数，不重复单词数）
    word_list = file_all_word.readlines()
    # 训练集中所有类中的单词总数，（txt中第一行）
    all_word_num = int(word_list[0].strip())

    # 对应类别的样本文档的（所有单词数，不重复单词数）
    word_list_item = word_list[index].strip().split(',')
    print word_list_item
    index_word = int(word_list_item[1])

    # 读入对应类别index的处理好的文件（单词 及对应的词频）
    path_fre = 'word_fre/index_fre/' + str(index) + '_fre.txt'
    file_fre = open(path_fre, 'r')
    word_fre_list = file_fre.readlines()

    # 单词 存在 word，词频 存在 fre_，计算每个单词对应的 P值，存在 word_p_dic 中
    # { word : p_index_word }
    # index_bayestraining.txt中
    word_p_dic = {}
    for word_fre in word_fre_list:
        word_fre = word_fre.strip().split(',')
        word = word_fre[0]
        fre_ = int(word_fre[1])
        p_index_word = float(fre_ + 1) / (index_word + all_word_num)
        word_p_dic[word] = p_index_word

    # 排序
    dic_list = sorted(word_p_dic.iteritems(), key=lambda asd: asd[1], reverse=True)
    path_outcome = 'train_result/' + str(index) + '_trainresult.txt'
    file_outcome = open(path_outcome, 'w')

    # 第一行写入所有单词个数 以及 单词词频和
    file_outcome.write(str(all_word_num) + ',' + str(index_word) + '\n')
    # 写入每个单词 以及对应的 P值
    i = 0
    for word_p in dic_list:
        file_outcome.write(word_p[0] + ',' + str(word_p[1]) + '\n')
        i = i + 1
    file_outcome.close


# 对训练素材进行预处理
prepare()
# 执行训练
for i in xrange(1, kinds+1):
    training(i)
    print str(i) + ' done';
