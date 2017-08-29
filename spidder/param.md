trainer.py 中的变量表

全局变量
all_frequency       array   所有训练集的单词数组
    （形如 [232,121,...]，数组中两个为一对，分别对应一种类别不重复的所有单词数，重复的所有单词数）

all_word            array   所有训练集的单词
    （形如 ['computer', 'artificial',...]，每个代表一个训练集中的单词）

path_file           string  文本地址路径



getWordFre()函数变量

text_frequency      int     该样本文档的所有单词的词频和（即去除停用词后单词数量）

text_word_dic           object  该样本文档的所有单词的词频表
    （形如 {'trainer': 23, 'classifier': 43, ...}）

path_index          string  该类别的文本的路径

file_index          file    path_index打开的文件

text                string  file_index读取到的文本内容

word_list           object  对text分词后的词对象

file_stop           file    停用词文件

stop_word_list      array   停用词数组

stop_word           string  stop_word_list 中的项



WriteFreFile()函数变量

text_word_dic_num       int     text_word_dic 的长度

word_list           object  排序后的词对象

path_index_fre      string  该类别的训练结果文件路径

file_index_fre      file    path_index_fre 打开的文件



prepare()函数变量

file_all_word       file    存放 all_word 所有训练集单词的文件

all_word_num        int     all_word 的长度



training()函数变量

path_all_word       string  all_word_num.txt的文件路径

file_all_word       file    path_all_word 打开的文件

word_list           array   all_word_num.txt中读取的内容

all_word_num        int     all_word_num.txt第一行的内容（第一行就是所有单词总数）

word_list_item      array   all_word_num.txt除第一行的每一行的内容

index_word          int     index对应的类别的所有单词数（不重复的也算）

path_fre            string  对应index类别的处理后的fre文件（即每个类别中各个单词及对应的词频）

file_fre            file    path_fre打开的文件

word_fre_list       array   对应index类别的 词频表

word_p_dic          object  存放每个单词和它的P值

word_fre            array  用于循环word_fre_list中的项    [单词, 词频]

word                string  word_fre中的“单词”部分

fre_                int     word_fre中的“词频”部分

p_index_word        float   每个单词的P值

dic_list            array   对计算好的P值表 进行排序后的表

path_outcome        string  输出结果文件的路径

file_outcome        file    path_outcome打开的文件
