# DouBanRecommend
基于豆瓣图书的推荐、知识图谱与知识引擎简单构建neo4j

本项目主要贡献源来自豆瓣爬虫（数据源）[lanbing510/DouBanSpider][1]、知识图谱引擎[Agriculture_KnowledgeGraph][2]、[apple.turicreate][3]中内嵌的推荐算法。
主要拿来做练习，数据来源可见[lanbing510/DouBanSpider][4]。

练习内容：

 - 豆瓣图书推荐 + 搜索模块
 - 豆瓣图书知识库简单应用（Neo4j的使用）

推荐与搜索模块再结合豆瓣内部的API就更加牛逼~~~！（[豆瓣API][11]）


----------


# 一、数据整理
简单的把爬虫数据进行简单的整理。主要做了一下针对每本书的评分，数据源中有两个值得用的字段：豆瓣书籍评分 + 书籍阅读人数，先等级化，然后进行平均，简单的得到了该书籍的得分。

    # 把豆瓣读书评分 / 豆瓣读书人群数量 进行分箱
    book_excel_all['rank_rank'] = pd.qcut(book_excel_all['rank'],10,duplicates ='drop',labels = False)
    book_excel_all['people_num_rank'] = pd.qcut(book_excel_all['people_num'],10,duplicates ='drop',labels = False)
    # 分箱之后，进行平均
    book_excel_all['scores'] = (book_excel_all['rank_rank'] + book_excel_all['people_num_rank'])/2

得到了如图的内容：
![此处输入图片的描述][6]
那么就开始做练习题啦~



----------


# 二、豆瓣图书推荐 + 搜索模块
推荐 + 搜索模块主要使用的是apple.turicreate模块的算法，那么该模块的使用可见：
[推荐模块︱apple.Turicreate个性化推荐recommender（五）][7]
简单贴个当时整理的图。

推荐算法 | 函数名 | 内容 |结果
:-------|:---------- |:---------- |:----------:
基于item相似推荐 | item_similarity_recommender | 有预测功能，item之间喜爱的相似程度。适用在给未知人群推荐的时候，可以寻找到item的相似对 | ![这里写图片描述](http://img.blog.csdn.net/20180105171438434?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvc2luYXRfMjY5MTczODM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
因式分解 | ranking_factorization_recommender以及factorization_recommender| **最常用,支持附加信息共同进模型** | ![这里写图片描述](http://img.blog.csdn.net/20180105171433995?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvc2luYXRfMjY5MTczODM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
基于内容的相似推荐 | item_content_recommender| 没有user概念，Item自己内容（多维度）决定，同类推荐，且没有点评数据可以提取的时候可以应用 | 数据格式不满足
项目流行度推荐 | item popularity| 基于项目流行程度来推荐，user不进入模型，缺点：并不能因人而异，受异常值影响较大 | ![这里写图片描述](http://img.blog.csdn.net/20180105171111411?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvc2luYXRfMjY5MTczODM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

主要内容见文件夹`book_recomend`.

本练习主要使用的算法是：基于item相似推荐

## 2.1 搜索模块：

- 输入：总表book_excel_all(book_excel.csv)

- 输出：搜索到的文档

- 算法：没有建模，主要是：先完全匹配；匹配不到，局部匹配，包含


简单展示一下最终结果：

    search_word = '机器学习'
    search(search_word,book_excel_all)

得到的结果可见：
![此处输入图片的描述][8]

## 2.2 推荐模块：

- 输入：总表book_excel_all(book_excel.csv)、基于类目item的推荐表(book_excel_name.csv)、搜索词（该搜索词一定时全的）

- 输出：相似图书推荐

- 目前使用的算法：apple.turicreate中的item_similarity_recommender推荐算法


简单展示一下所写的功能：

    search_word = '浪潮之巅'
    item_recomend(search_word,book_excel_all,recomend_item,topn = 10)

结果：
![此处输入图片的描述][9]

## 2.3 推荐对应表生成模块
根据核心数据源，利用apple.turicreate平台的基于item的推荐，主要是以书籍类别为主要筛选对象，对书籍类别进行相关推荐，输入信息表，输出相关推荐表格。如表格:`item_data_item.csv`


----------


# 三、豆瓣图书知识库简单应用（Neo4j的使用）

借用neo4j简单的实践了一下：neo4j的docker启动、数据导入模块、py2neo查询模块。



**练习的时候有些心得：**

- 保证节点的唯一性

    犯错：在book_excel，书名信息是不唯一的，可能一本书既可能被归类到 旅游、哲学、编程、创业
    
- 其他心得：
    
    （1）从效果来看，如果关系类型比较少，比较适合直接用多表合一的方式进行查询；
    
    知识图谱中的图数据库的查询，建立在关系错综复杂、才有查询必要。
    
    （2）图数据库，一定要对节点 + 关系去重
    
    
- 时间消耗：
    
    3W节点 - 25.7W关系 - 3h时间 - 1002MB


----------


## 3.1 neo4j的docker启动
neo4j开启的一种方法就是docker启动，neo4j的docker下载地址：https://hub.docker.com/_/neo4j/

笔者在使用neo4j的使用会遇到几个问题：

 - neo4j的内存默认设置太小，需要手动扩大
 - 数据导入模块
 - 已经导入的数据怎么保存

因为本地数据导入neo4j之中，最好把数据放在指定目录之中，于是乎在docker启动之前就可以设置一下：

    docker run \
        --publish=7474:7474 --publish=7687:7687 \
        --volume=/matt/neo4j:/var/lib/neo4j/import  --rm -ti neo4j bash
其中`/matt/neo4j`是宿主机的目录，`/var/lib/neo4j/import`是docker之中本地导入csv的路径，那么这样就可以直接使用：`LOAD CSV WITH HEADERS  FROM "file:///book_excel_name.csv" AS line`

扩大内存的话，就需要到`/neo4j/conf/neo4j.conf`之中修改以下参数：

    dbms.memory.heap.initial_size = 1024G 
    dbms.memory.heap.max_size= 1024G
    dbms.memory.pagecache.size = 10240M # 缓存，可以调制到一些

在docker 之中开启neo4j为：

    /var/lib/neo4j/bin/neo4j start

打开之后需要等待一段时间的启动。

![此处输入图片的描述][10]

**已经导入的数据怎么保存？**

备份Neo4j的数据:

    1)停掉数据库.
    
    2)备份D:\Neo4J\neo4j-enterprise-1.9.1\data目录下graph.db目录中的所有内容.
    
    3)在服务器上拷贝graph.db目录中的内容到新的服务器的相同目录中,启动即可.


----------


## 3.2 数据导入模块

为了确保唯一性，所以导入的时候，书名节点、书类别节点、出版社节点都是唯一的，同时建立了书籍-类型的关系。

    // 导入书名节点
    LOAD CSV WITH HEADERS  FROM "file:///book_excel_name.csv" AS line
    CREATE (:BookNode { name:line.book_name,rank:line.rank,people_num:line.people_num, author:line.author,public_infos:line.public_infos,public_time:line.public_time,price:line.price })
    
    // 导入书类别节点
    LOAD CSV WITH HEADERS  FROM "file:///book_excel_type.csv" AS line
    CREATE (:BookType { type:line.type })
    // MATCH (n:BookType) OPTIONAL MATCH (n)-[r]-() DELETE n,r // 删除命令
    
    // 导入书出版社节点
    LOAD CSV WITH HEADERS  FROM "file:///book_excel_public.csv" AS line
    CREATE (:BookPub { pub:line.public })
    // MATCH (n:BookPub) OPTIONAL MATCH (n)-[r]-() DELETE n,r //删除命令
    
    //建立关系:书-类型
    LOAD CSV WITH HEADERS  FROM "file:///book_excel.csv" AS line
    MATCH (entity1:BookNode{name:line.book_name}), (entity2:BookType{type:line.type})
    CREATE (entity1)-[:RELATION_TYPE]->(entity2);

这边导入的时候发现有些重复关系，懒... 就不改了...


## 3.3 py2neo查询模块

主要数据可见：douban_kg文档

    from py2neo import Node, Relationship, Graph
    graph = Graph(
        "http://localhost:7474", 
        username="neo4j", 
        password="qwer@1234"
    )

通过py2neo先链接neo4j数据库。同时：


    # 查询书目内容
    graph.find_one(label="BookNode",property_key="name",property_value='计算机视觉')
        # label代表：标签
        # property_key代表：节点属性
        # property_value代表：具体属性名称
    
    
    # 查询书目-类型
    graph.data("MATCH (entity1) - [:RELATION_TYPE] -> (entity2)  WHERE entity2.ytpe = '旅行' RETURN rel,entity2")


  [1]: https://github.com/lanbing510/DouBanSpider
  [2]: https://github.com/mattzheng/Agriculture_KnowledgeGraph
  [3]: https://github.com/apple/turicreate
  [4]: https://github.com/lanbing510/DouBanSpider
  [5]: https://pan.baidu.com/s/1DhWIdLBaPdHcO94DMRPzwA
  [6]: https://github.com/mattzheng/DouBanRecommend/blob/master/douban_kg/book_2.png
  [7]: https://blog.csdn.net/sinat_26917383/article/details/78979830
  [8]: https://github.com/mattzheng/DouBanRecommend/blob/master/douban_kg/book1.png
  [9]: https://github.com/mattzheng/DouBanRecommend/blob/master/douban_kg/book_2.png
  [10]: https://github.com/mattzheng/DouBanRecommend/blob/master/douban_kg/book3.png
  [11]: https://developers.douban.com/wiki/?title=api_v2
