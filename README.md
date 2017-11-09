# spider-classifier-system
爬虫+分类


# 爬虫
爬虫使用的是Python的request 和 BeatifulSoup库
#### json格式
spider/spider_to_json.py
爬取的文件存于../spider_json文件夹中
#### txt格式
spider/spider_to_txt.py
爬取的文件存于../spider_txt文件夹中



# 分类器
## 原理

### 贝叶斯公式  
![公式名](http://latex.codecogs.com/png.latex?P(B|A)=\frac{P(A|B)P(B)}{P(A)})  

有分类集合C = { ![公式名](http://latex.codecogs.com/png.latex?C_{1}C_{2}...C_{n}) }  
则文本D属于 ![公式名](http://latex.codecogs.com/png.latex?C_{i}) 的概率为  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![公式名](http://latex.codecogs.com/png.latex?P(C_{i}|D)=\frac{P(D|Ci)P(C_{i})}{P(D)}=\frac{P(D|Ci)}{P(C_{i})P(D)})  
因为 ![公式名](http://latex.codecogs.com/png.latex?P(C_{i})=1/n),&nbsp;&nbsp;![公式名](http://latex.codecogs.com/png.latex?P(D))都相等  
所以 ![公式名](http://latex.codecogs.com/png.latex?P(C_{i}|D)) 可视为 ![公式名](http://latex.codecogs.com/png.latex?P(D|C_{i}))  

假设文本D的特征符合集合X，有m个特征:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
X = {![公式名](http://latex.codecogs.com/png.latex?{X_{1},X_{2},...,X_{m}})}  
那么  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![公式名](http://latex.codecogs.com/png.latex?P(D|C_{i})=P(X_{1}|C_{i})P(X_{2}|C_{i})...P(X_{m}|C_{i}))

### 多项式模型
##### 朴素贝叶斯分类器有两种常见模型：多项式模型 和 伯努利模型  
两者的区别在于伯努利模型统计的时候忽略了特征词在文档中出现的次数，都算作一次。而多项式模型是以“词”为统计单位，当某个特征词在文档中出现多次的时候，与伯努利模型相反，多项式模型算作多次。  
因此多项式模型更符合作为文本分类的想法
#### 多项式模型原理
朴素贝叶斯多项式模型的原理是：设文本D = (t_1, t_2,..., t_m), t_m是该文档中出现过的单词，允许重复，步骤如下：
>计算文本类别的先验概率：  
  P(C) = 类别C中出现的单词总数/整个训练样本的单词总数  
计算单词t_m在类别C下的类条件概率：  
  P(t_m|C) = (类别C中单词t_m 在各个文本中出现过的次数之和)/(类别C中的单词总数 + 所有训练样本的单词数)   (a取值范围[0,1]，一般取1,避免单词t_m次数是0)  
计算待分类分本A被判别为类别C_i的后验概率，假设A中的词A_1, A_2,…, A_k相互独立：  
  P(C_i|A) = (P(C_i )P(A_1 |C_i)P(A_2 |C_i)…P(A_k |C_i))/(P(A))  

`先验条件可以认为是类别C在整体上占多大比例  
类条件概率可以认为是单词tm在证明文本D属于类别C上提供了多大的证据
后验概率可以认为是文本D和类别C的关联度`

因为对于同一文档P(A)一样，所以只需要比较分子，以后验概率最大的类别为文档A所属的类别。
根据朴素贝叶斯多项式模型的原理，训练器完成对爬取文本进行分词的预处理工作、计算每个类别的先验概率、计算类中单词的类条件概率；分类器完成计算待分类文本在各类别的后验概率并比较出最接近的类别。



## 训练器
### 预处理
操作 | 文件
---|---
计算各个类别的所有训练文本的词频和，词频表 |
记录各个类别的词频表 | `index_fre.json`
记录各个类别的单词总数，词频和 | `all_word_num.json`
记录所有训练样本的单词总数 | `all_word_num.json`

### 训练
操作 | 文件
---|---
计算各个类别每个单词的类条件概率表，并记录 | `index_bayestraining.json`

### 分类器
操作 | 文件
---|---
处理待分类文本，取得该文本的单词列表 |
从文件中读取各个类别的类条件概率表 | `index_bayestraining.json`
对待分类文本的单词与各个类别进行比较，计算 |
&nbsp;&nbsp;&nbsp;&nbsp;若单词在该类别的表中，则用对应的概率 |
&nbsp;&nbsp;&nbsp;&nbsp;若单词不在该类别的表中，则计算 1/(所有训练样本的单词数 + 词频和) |
最终取得的结果即为该文本与类别的关联度，关联度最大的即视为该文本所属的类别，并记录 | `classify_result.json`


# Elasticsearch
## 环境搭建
#### 运行Elasticsearch
进入	/elasticsearch-5.5.2/ 文件夹  
运行	`./bin/elasticsearch` 将ES开启  
打开浏览器	输入 `localhost:9200/`	即可看到成功运行的案例

#### 运行插件 elasticsearch-head
进入	elasticsearch-head 文件夹  
运行	`npm run start`  
打开浏览器	输入 `localhost:9100/`	显示的就是head插件的页面

#### 注意，如果是新机器上，需要重新安装Elasticsearch和head插件
Elasticsearch 安装地址为 https://www.elastic.co/downloads/elasticsearch
head 插件安装地址为 https://github.com/mobz/elasticsearch-head

## 对于可能出现的集群健康值 ：yellow
执行  curl -XPUT "http://localhost:9200/_settings" -d' { "number_of_replicas" : 0 } '
得到  {"acknowledged":true}


## 操作
#### 批量导入
要批量导入的数据以下面这种格式保存  
```
{'index': {'_index': 'papers', '_type': u'artificial', '_id': 1}}
{'title': 'Dk', 'authors': ['darkindom'], 'abstract': "this is Dk's paper.", 'fields': 'darkindom'}
```
然后执行下面这个命令  
`curl -s -XPOST localhost:9200/_bulk --data-binary @data.json`  
可以看到data.json里的内容已经导入到es里了

#### 数据处理
数据存放于es中，包括分类完的数据  
通过发送请求进行操作：  
> 新增 put  `localhost:9200/index/type/id`  
修改 post  `localhost:9200/index/type/id`  
删除 delete  `localhost:9200/index/type/id`  
搜索 post  `localhost:9200/index/type/_search`  

## 注意事项

更改ip地址后，需要及时更改 /elasticsearch-5.5.2/config/elasticsearch.yml 中对应的ip地址

# 可视化界面
## 服务器
服务器是用nodeJS搭建的，同时需要注意连接es的ip地址也要及时更改为现在的地址
### 跨域问题
因为es库和服务器在不同的端口，所以需要解决跨端口问题，这里使用的方法是：  
nodeJS的 proxy
把发送向 /papers/* 的请求转到9200端口上

## 客户端
