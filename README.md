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

### 2.2 数据分析

* 读取前10000条JSON_LINE便于数据分析
* 读取所有的Propery_JSON_LINE用于Claims链接

### 2.3 数据预处理

* 进行Data Laundry 以删除不需要的数据
* 保留中文和英文的数据

### 2.4 Mysql的设计

* 为Mysql设计E-R图
* 将数据存入Mysql
* 设计SQL语句对Mysql进行查询

### 2.5 gStore的设计

* 为gStore生成对应的三元组
* 将数据存入gStore
* 设计Sparql语句对Mysql进行查询

### 2.6 Mysql与gStore对比

* 对关系型数据库和图数据库进行对比

### 2.7 Gui的设计

* 使用C#设计了一款可以进行知识问答的APP

## 三、数据获取

Linux:
* wget https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2

Win10: 
* https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2

## 四、数据分析
* 读取前10000行作为数据源
* 在磁盘空间足够的情况下，可增加数据量大小
* 在方法上是一致的
* 毕竟学习的目的在于学习，而不是折磨

* 整理出10000条qitem进行语义理解
```
python line_10000_load.py --wikidata_path your_bz_path --store_path your_store_path
```

* 整理出所有的Property进行语义理解
```
python find_pid.py --pretreat_path your_bz_path --store_path your_store_path
```
### 通过在线json解析可以看出Q_item的格式如下

![avater](https://github.com/Howdy-Personally/tips_of_wikidata/blob/main/pic/qitem.png)

### 与此同时pitem的格式如下

![avater](https://github.com/Howdy-Personally/tips_of_wikidata/blob/main/pic/pitem.png)

### 每个P或Q下面有一个claims

![avater](https://github.com/Howdy-Personally/tips_of_wikidata/blob/main/pic/claims.png)
### claims下包含mainsnak,qualifiers,references,并分别包含如下属性
* mainsnak:

![avater](https://github.com/Howdy-Personally/tips_of_wikidata/blob/main/pic/mainsnak.png)
* qualifiers:

![avater](https://github.com/Howdy-Personally/tips_of_wikidata/blob/main/pic/qualifiers.png)
* references:

![avater](https://github.com/Howdy-Personally/tips_of_wikidata/blob/main/pic/references.png)
## 五、数据预处理

* 数据清洗
* 对qitem进行数据清洗
* 对pid进行数据清洗
* 生成易于理解的英文数据和中文数据

### 将JSON数据整理，得到如下的数据结构图
![avater](https://github.com/Howdy-Personally/tips_of_wikidata/blob/main/pic/structure.png)



## 六、Mysql设计
### 完成了数据分析预处理之后，在Mysql设计思路中，采用如下ER图结构。
![avater](https://github.com/Howdy-Personally/tips_of_wikidata/blob/main/pic/db_struct.png)

### 将qitem和pid存入mysql中

```
python store_to_db.py --qitem_path your_qitem_path --pid_path your_pid_path
```
### 在i5-10400 500G-M.2 16G-Memory配置下耗时：7h-48m-45s

### 日志文本：
---
#### Sun May 30 10:13:38 2021 store start
#### Sun May 30 12:22:22 2021 line 5000 entitles stored
#### Sun May 30 16:15:22 2021 line 10000 entitles stored
#### Sun May 30 16:15:22 2021 and line 10000 entitles all stored
#### Sun May 30 17:02:50 2021 and line 4000 properties stored
#### Sun May 30 17:50:52 2021 and line 8000 properties stored
#### Sun May 30 18:02:23 2021 and line 8755 properties all stored
#### Sun May 30 18:02:23 2021 store end
---

## 七、gStore的设计
---
#### 大部分知识图谱使用RDF描述世界上的各种资源，并以三元组的形式保存到知识库中。gStore也不例外，它也使用RDF语言，有利于在网络上形成人机可读，并可由机器自动处理的文件。
#### RDF的基本资料模型包括了三个对象类型："资源"，"属性"，"陈述"。换句话说就是"主"，"谓"，"宾"。
---
### 基于这种考虑，将数据结构设计成如下模式
![avater](https://github.com/Howdy-Personally/tips_of_wikidata/blob/main/pic/rdf.png)

### 将qitem和pid的json文档转换为RDF文档
```
python json_to_rdf.py --qitem_path your_qitem_path --pid_path your_pid_path
```

### 在i5-10400 500G-M.2 16G-Memory配置下耗时：3m-28s

### 日志文本：
---
#### Mon May 31 09:35:22 2021 rdf store start
#### Mon May 31 09:36:42 2021 line 5000 stored
#### Mon May 31 09:38:01 2021 line 10000 stored
#### Mon May 31 09:38:01 2021 and line 10000 entitles all stored
#### Mon May 31 09:38:23 2021 and line 4000 stored
#### Mon May 31 09:38:46 2021 and line 8000 stored
#### Mon May 31 09:38:50 2021 and line 8755 properties all stored
#### Mon May 31 09:38:50 2021 rdf store end
---
### 但其实在转换为rdf文档时，可能会存在数据重复，因而需要采取去重操作
```
python duplicate_removal.py --dirty_path your_dirty_path --out_path your_out_path
```
### 然而去重操作非常费时，也可以选择不进行去重
---
关系型数据库和图数据库的主要差异是数据存储的方式。关系型数据天然就是表格式的，因此存储在数据表的行和列中。数据表可以彼此关联协作存储，也很容易提取数据。
与其相反，非关系型数据不适合存储在数据表的行和列中，而是大块组合在一起，图结构数据及其特性是选择数据存储和提取方式的首要影响因素。

---

## 八、Mysql与gStore对比
### 对于mysql而言，使用sql语句查询mysql，使用如下的查询语句，得到了一个关于Belgium和P123属性的数据库表
### 耗时1ms

---

#### SELECT ?x?y?z
#### WHERE
#### {&lt;Belgium&gt; &lt;P123&gt; ?x.}

---
### 对于gStore而言，使用sparql语句查询知识图谱，使用如下的查询语句，得到了一个关于Belgium和P123属性的所有结点知识图谱
### 耗时1ms

---

#### SELECT ?x?y?z
#### WHERE
#### {&lt;Belgium&gt; &lt;P123&gt; ?x.}

---


![avater](https://github.com/Howdy-Personally/tips_of_wikidata/blob/main/pic/belgium_gstore.png)


### 耗时5ms

---

#### SELECT ?x?y?z
#### WHERE
#### {&lt;Belgium&gt; &lt;P123&gt; ?x.
#### ?y?z?x.}

---

![avater](https://github.com/Howdy-Personally/tips_of_wikidata/blob/main/pic/gStore.png)



## 九、结论和讨论

### 通过上面的数据存储和数据查询操作，可以显而易见的看出，对于关系数据库而言，数据查找在效率上并没有优势，反而是拖后腿的，但是数据更加直观
### 而对于图数据库，可以看出再查询效率上很高，可视化程度也很清晰，但是对于数据的绑定稍显复杂，如果三元组设计的不够好的话反而会出现找不到数据的情况

