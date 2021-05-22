智能数据工程实验报告
====================

- 学院：信息学院
- 专业：电子信息
- 姓名：潘森垒
- 学号：12020215212


> [作业要求](作业要求.md)


## 一、项目名称
基于Mysql关系数据库与gStore图数据库的数据查询对比实验

## 二、项目任务和问题
### 2.1 数据获取

* From Wikidata Dowload JSON.bz2

### 2.2 数据预处理
* 读取前100条JSON_LINE便于数据分析
* 进行Data Laundry 以删除不需要的数据
* Json.dumps 对数据进行整理
* 
### 2.3 Mysql的设计
* 为Mysql设计E-R图
* 将数据存入Mysql
* 设计SQL语句对Mysql进行查询
* 
### 2.4 gStore的设计
* 为gStore生成对应的三元组
* 将数据存入gStore
* 设计Sparql语句对Mysql进行查询

### 2.5 Mysql与gStore对比
* 对关系型数据库和图数据库进行对比

### 2.6 Gui的设计
* 使用C#设计了一款可以进行知识问答的APP

## 三、数据获取
Linux:
* wget https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2
Win10: 
* https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2
## 四、数据集和评测指标


## 五、实证分析和测试结果


## 六、结论和讨论
