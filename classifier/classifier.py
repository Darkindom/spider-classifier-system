#!usr/bin/python
# -*- coding:utf-8 -*-

import os, sys
import math
import jieba
import word_is_num
import json

path_file = os.path.abspath(sys.argv[0])
path_file=os.path.dirname(path_file) + '/'
print path_file

kinds = 8


def getPofClass(index, word_list):
    # 输入类index的贝叶斯训练结果文件
    path_train = path_file + 'train_result/' + str(index) + '_trainresult.txt'
    file_train = open(path_train, 'r')
    dic_train = {}   # 存储 index_bayestraining.txt 中的 (单词：P)
    train_word = file_train.readlines()
    word_fre_num = train_word[0].strip() #index_bayestraining.txt的第一行
    word_fre = int(word_fre_num[1])    #所有样本的所有单词的词频
    word_num = int(word_fre_num[0])    #所有样本的所有单词个数
    for i in xrange(1, len(train_word)):
        word_p = train_word[i].strip().split(',')
        dic_train[word_p[0]] = float(word_p[1])

    #遍历测试样本的wordlist，求每个Word的p
    p_list = []
    for word in word_list:
        word = word.strip()
        if word in dic_train:
            p_list.append(str(dic_train[word]))
        else:
            p_list.append(str(1.0 / (word_fre + word_num)))
    #计算P
    p_index = 0
    for p in p_list:
        p = math.log(float(p), 2)
        p_index = p_index + p
    return -p_index


def bayes(text):
    # 分词
    word_list = jieba.cut(text, cut_all=False)

    # 停用词
    stopword_path = path_file + 'data/stop.txt'
    file_stopword = open(stopword_path, 'r')
    stopword_list = file_stopword.readlines()
    for i in xrange(0, len(stopword_list)):
        word = stopword_list[i].strip()
        stopword_list[i] = word

    # 去停用词
    word_list_nostop = []
    for word in word_list:
        word = word.strip().encode('utf-8')
        if word_is_num.is_number(word) or word in stopword_list:
            pass
        else:
            word_list_nostop.append(word)

    # 求每个类index的P值，最大P值的类别 为最匹配text的类别
    max = 0
    maxIndex = 0
    for index in xrange(1, kinds+1):
        y = getPofClass(index, word_list_nostop)
        if y != float("inf") and y > max:
            max = y
            maxIndex = index
    return maxIndex


def classify():
    all_count = 0
    right_count = 0
    file_text = open(path_file + 'data/wait_to_classify_text.json', "r")
    item = json.load(file_text)
    wait_classify_text = item['data']
    file_text.close

    file_outcome = open(path_file + 'classify_result.txt', 'w')
    for item in wait_classify_text:
        text = item['abstract']
        text = text.strip()
        if len(text) == 0:
            continue
        all_count += 1

        # 对text进行分类，得到对应的类别index
        getIndex = bayes(text)

        print str(item['title']) + "\nclassify kind : " + str(getIndex)
        file_outcome.write(str(getIndex) + '\n')
    file_outcome.close


# 执行分类函数
classify()
