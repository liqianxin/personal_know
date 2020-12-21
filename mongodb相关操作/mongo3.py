5. 查询
    # 查询 age 小于 15 的
    for u in db.users.find({"age":{"$lt":15}}): print u

  5.1 查询一条记录
    # 查询 name 等于 user8 的
    for u in db.users.find({"name":"user8"}): print u

    # 获取查询的一个
    u2 = db.users.find_one({"name":"user9"}) # 查不到时返回 None
    print u2

  5.2 查询特定键 (fields)
    # select name, age from users where age = 21
    for u in db.users.find({"age":21}, ["name", "age"]): print u
    for u in db.users.find(fields = ["name", "age"]): print u

  5.3 排序(SORT)
    pymongo.ASCENDING  # 也可以用 1 来代替
    pymongo.DESCENDING # 也可以用 -1 来代替
    for u in db.users.find().sort([("age", pymongo.ASCENDING)]): print u   # select * from 集合名 order by 键1
    for u in db.users.find().sort([("age", pymongo.DESCENDING)]): print u  # select * from 集合名 order by 键1 desc
    for u in db.users.find().sort([("键1", pymongo.ASCENDING), ("键2", pymongo.DESCENDING)]): print u # select * from 集合名 order by 键1 asc, 键2 desc
    for u in db.users.find(sort = [("键1", pymongo.ASCENDING), ("键2", pymongo.DESCENDING)]): print u # sort 的另一种写法
    for u in db.users.find({"name":"user9"}, sort=[['name',1],['sex',1]], fields = ["name", "age", 'sex']): print u  # 组合写法

  5.4 从第几行开始读取(SLICE)，读取多少行(LIMIT)
    # select * from 集合名 skip 2 limit 3
    # MySQL 的写法： select * from 集合名 limit 2, 3
    for u in db.users.find().skip(2).limit(3): print u
    for u in db.users.find(skip = 2, limit = 3): print u

    # 可以用切片代替 skip & limit (mongo 中的 $slice 貌似有点问题)。
    for u in db.users.find()[2:5]: print u

    # 单独的写
    for u in db.users.find().skip(2): print u
    for u in db.users.find(skip=1): print u
    for u in db.users.find().limit(5): print u
    for u in db.users.find(limit = 3): print u

  5.5 多条件查询(Conditional Operators)    # like 的可使用正则表达式查询
    # select * from users where name = 'user3' and age > 12 and age < 15
    for u in db.users.find({'age': {'$gt': 12, '$lt': 15}, 'name': 'user3'}): print u
    # select * from users where name = 'user1' and age = 21
    for u in db.users.find({"age":21, "name":"user1"}): print u

  5.6 IN
    for u in db.users.find({"age":{"$in":(23, 26, 32)}}): print u   # select * from users where age in (23, 26, 32)
    for u in db.users.find({"age":{"$nin":(23, 26, 32)}}): print u  # select * from users where age not in (23, 26, 32)

  5.7 统计总数(COUNT)
    print(db.users.count())  # select count(*) from users
    print(db.users.find({"age":{"$gt":30}}).count()) # select count(*) from users where age > 30

  5.8 OR
    for u in db.users.find({"$or":[{"age":25}, {"age":28}]}): print u  # select * from 集合名 where 键1 = 值1 or 键1 = 值2
    for u in db.users.find({"$or":[{"age":{"$lte":23}}, {"age":{"$gte":33}}]}): print u  # select * from 集合名 where 键1 <= 值1 or 键1 >= 值2
  6. 是否存在 (exists)
    db.users.find({'sex':{'$exists':True}})  # select * from 集合名 where exists 键1
    db.users.find({'sex':{'$exists':False}}) # select * from 集合名 where not exists 键1

  7. 正则表达式查询
    for u in db.users.find({"name" : {"$regex" : r"(?i)user[135]"}}, ["name"]): print u # 查询出 name 为 user1, user3, user5 的

  8. 多级路径的元素值匹配
    Document 采取 JSON-like 这种层级结构，因此我们可以直接用嵌入(Embed)代替传统关系型数据库的关联引用(Reference)。
    MongoDB 支持以 "." 分割的 namespace 路径，条件表达式中的多级路径须用引号

    # 如果键里面包含数组，只需简单匹配数组属性是否包含该元素即可查询出来
    db.集合名.find_one({'address':"address1"}) # address 是个数组，匹配时仅需包含有即可
    # 查询结果如：{"_id" : ObjectId("4c479885089df9b53474170a"), "name" : "user1", "address" : ["address1", "address2"]}

    # 条件表达式中的多级路径须用引号,以 "." 分割
    u = db.集合名.find_one({"im.qq":12345678})
    # 查询结果如：{"_id" : ObjectId("4c479885089df9b53474170a"), "name" : "user1", "im" : {"msn" : "user1@hotmail.com", "qq" : 12345678}}

    print u['im']['msn']  #显示： user1@hotmail.com

    # 多级路径的更新
    db.集合名.update({"im.qq":12345678}, {'$set':{"im.qq":12345}})

    # 查询包含特定键的
    for u in db.users.find({"im.qq":{'$exists':True}}, {"im.qq":1}): print u
    # 显示如： { "_id" : ObjectId("4c479885089df9b53474170a"), "im" : { "qq" : 12345 } }


    for u in db.users.find({'data':"abc"}): print u
    # 显示如： { "_id" : ObjectId("4c47a481b48cde79c6780df5"), "name" : "user8", "data" : [ { "a" : 1, "b" : 10 }, 3, "abc" ] }
    for u in db.users.find({'data':{'$elemMatch':{'a':1, 'b':{'$gt':5}}}}): print u
    # 显示如： { "_id" : ObjectId("4c47a481b48cde79c6780df5"), "name" : "user8", "data" : [ { "a" : 1, "b" : 10 }, 3, "abc" ] }
    {data:"abc"} 仅简单匹配数组属性是否包含该元素。$elemMatch 则可以处理更复杂的元素查找条件。当然也可以写成如下方式：
    db.集合名.find({"data.a":1, "data.b":{'$gt':5}})

    对数组, 还可以直接使用序号进行操作：
    db.集合名.find({"data.1":3}) # 序号从0开始


    # 如集合的一列内容
    {"classifyid":"test1",
          "keyword":[
                {"name":'test1', # 将修改此值为 test5 (数组下标从0开始,下标也是用点)
                "frequence":21,
                },
                {"name":'test2', # 子表的查询，会匹配到此值
                "frequence":50,
                },
          ]
    }
    # 子表的修改(子表的其它内容不变)
    db.集合名.update({"classifyid":"test1"}, {"$set":{"keyword.0.name":'test5'}})
    # 子表的查询
    db.集合名.find({"classifyid":"test1", "keyword.0.name":"test2"})
	
	
	(1) $all: 判断数组属性是否包含全部条件。
    db.users.insert({'name':"user3", 'data':[1,2,3,4,5,6,7]})
    db.users.insert({'name':"user4", 'data':[1,2,3]})

    for u in db.users.find({'data':{'$all':[2,3,4]}}): print u
    # 显示： { "_id" : ObjectId("4c47a133b48cde79c6780df0"), "name" : "user3", "data" : [ 1, 2, 3, 4, 5, 6, 7 ] }
    注意和 $in 的区别。$in 是检查目标属性值是条件表达式中的一员，而 $all 则要求属性值包含全部条件元素。

  (2) $size: 匹配数组属性元素数量。
    for u in db.users.find({'data':{'$size':3}}): print u
    # 只显示匹配此数组数量的： { "_id" : ObjectId("4c47a13bb48cde79c6780df1"), "name" : "user4", "data" : [ 1, 2, 3 ] }

  (3) $type: 判断属性类型。
    for u in db.users.find({'t':{'$type':1}}): print u  # 查询数字类型的
    for u in db.users.find({'t':{'$type':2}}): print u  # 查询字符串类型的

    类型值:
        double:1
        string: 2
        object: 3
        array: 4
        binary data: 5
        object id: 7
        boolean: 8
        date: 9
        null: 10
        regular expression: 11
        javascript code: 13
        symbol: 14
        javascript code with scope: 15
        32-bit integer: 16
        timestamp: 17
        64-bit integer: 18
        min key: 255
        max key: 127

  (4) $not: 取反，表示返回条件不成立的文档。
    似乎只能跟正则和 $mod 一起使用？？？？
    # 还不知如何使用

  (5) $unset: 和 $set 相反，表示移除文档属性。
    for u in db.users.find({'name':"user1"}): print u
    # 显示如： { "_id" : ObjectId("4c479885089df9b53474170a"), "name" : "user1", "age" : 15, "address" : [ "address1", "address2" ] }

    db.users.update({'name':"user1"}, {'$unset':{'address':1, 'age':1}})
    for u in db.users.find({'name':"user1"}): print u
    # 显示如： { "_id" : ObjectId("4c479885089df9b53474170a"), "name" : "user1" }

  (6) $push: 和 $ pushAll 都是向数组属性添加元素。# 好像两者没啥区别
    for u in db.users.find({'name':"user1"}): print u
    # 显示如： { "_id" : ObjectId("4c479885089df9b53474170a"), "age" : 15, "name" : "user1" }

    db.users.update({'name':"user1"}, {'$push':{'data':1}})
    for u in db.users.find({'name':"user1"}): print u
    # 显示如： { "_id" : ObjectId("4c479885089df9b53474170a"), "age" : 15, "data" : [ 1 ], "name" : "user1" }

    db.users.update({'name':"user1"}, {'$pushAll':{'data':[2,3,4,5]}})
    for u in db.users.find({'name':"user1"}): print u
    # 显示如： { "_id" : ObjectId("4c479885089df9b53474170a"), "age" : 15, "data" : [ 1, 2, 3, 4, 5 ], "name" : "user1" }

  (7) $addToSet: 和 $push 类似，不过仅在该元素不存在时才添加 (Set 表示不重复元素集合)。
    db.users.update({'name':"user2"}, {'$unset':{'data':1}})
    db.users.update({'name':"user2"}, {'$addToSet':{'data':1}})
    db.users.update({'name':"user2"}, {'$addToSet':{'data':1}})
    for u in db.users.find({'name':"user2"}): print u
    # 显示： { "_id" : ObjectId("4c479896089df9b53474170b"), "data" : [ 1 ], "name" : "user2" }

    db.users.update({'name':"user2"}, {'$push':{'data':1}})
    for u in db.users.find({'name':"user2"}): print u
    # 显示： { "_id" : ObjectId("4c479896089df9b53474170b"), "data" : [ 1, 1 ], "name" : "user2" }

    要添加多个元素，使用 $each。
    db.users.update({'name':"user2"}, {'$addToSet':{'data':{'$each':[1,2,3,4]}}})
    for u in db.users.find({'name':"user2"}): print u
    # 显示： {u'age': 12, u'_id': ObjectId('4c479896089df9b53474170b'), u'data': [1, 1, 2, 3, 4], u'name': u'user2'}
    # 貌似不会自动删除重复

  (8) $each 添加多个元素用。
    db.users.update({'name':"user2"}, {'$unset':{'data':1}})
    db.users.update({'name':"user2"}, {'$addToSet':{'data':1}})
    for u in db.users.find({'name':"user2"}): print u
    # 显示： { "_id" : ObjectId("4c479896089df9b53474170b"), "data" : [ 1 ], "name" : "user2" }

    db.users.update({'name':"user2"}, {'$addToSet':{'data':{'$each':[1,2,3,4]}}})
    for u in db.users.find({'name':"user2"}): print u
    # 显示： {u'age': 12, u'_id': ObjectId('4c479896089df9b53474170b'), u'data': [1, 2, 3, 4], u'name': u'user2'}

    db.users.update({'name':"user2"}, {'$addToSet':{'data':[1,2,3,4]}})
    for u in db.users.find({'name':"user2"}): print u
    # 显示： { "_id" : ObjectId("4c479896089df9b53474170b"), "data" : [ 1, 2, 3, 4, [ 1, 2, 3, 4 ] ], "name" : "user2" }

    db.users.update({'name':"user2"}, {'$unset':{'data':1}})
    db.users.update({'name':"user2"}, {'$addToSet':{'data':[1,2,3,4]}})
    for u in db.users.find({'name':"user2"}): print u
    # 显示： { "_id" : ObjectId("4c47a133b48cde79c6780df0"), "data" : [ [1, 2, 3, 4] ], "name" : "user2" }

  (9) $pop: 移除数组属性的元素(按数组下标移除)，$pull 按值移除，$pullAll 移除所有符合提交的元素。
    db.users.update({'name':"user2"}, {'$unset':{'data':1}})
    db.users.update({'name':"user2"}, {'$addToSet':{'data':{'$each':[1, 2, 3, 4, 5, 6, 7, 2, 3 ]}}})
    for u in db.users.find({'name':"user2"}): print u
    # 显示： { "_id" : ObjectId("4c47a133b48cde79c6780df0"), "data" : [ 1, 2, 3, 4, 5, 6, 7, 2, 3 ], "name" : "user2" }

    db.users.update({'name':"user2"}, {'$pop':{'data':1}}) # 移除最后一个元素
    for u in db.users.find({'name':"user2"}): print u
    # 显示： { "_id" : ObjectId("4c47a133b48cde79c6780df0"), "data" : [ 1, 2, 3, 4, 5, 6, 7, 2 ], "name" : "user2" }

    db.users.update({'name':"user2"}, {'$pop':{'data':-1}}) # 移除第一个元素
    for u in db.users.find({'name':"user2"}): print u
    # 显示： { "_id" : ObjectId("4c47a133b48cde79c6780df0"), "data" : [ 2, 3, 4, 5, 6, 7, 2 ], "name" : "user2" }

    db.users.update({'name':"user2"}, {'$pull':{'data':2}}) # 移除全部 2
    for u in db.users.find({'name':"user2"}): print u
    # 显示： { "_id" : ObjectId("4c47a133b48cde79c6780df0"), "data" : [ 3, 4, 5, 6, 7 ], "name" : "user2" }

    db.users.update({'name':"user2"}, {'$pullAll':{'data':[3,5,6]}}) # 移除 3,5,6
    for u in db.users.find({'name':"user2"}): print u
    # 显示： { "_id" : ObjectId("4c47a133b48cde79c6780df0"), "data" : [ 4, 7 ], "name" : "user2" }

  (10) $where: 用 JS 代码来代替有些丑陋的 $lt、$gt。
    MongoDB 内置了 Javascript Engine (SpiderMonkey)。可直接使用 JS Expression，甚至使用 JS Function 写更复杂的 Code Block。

    db.users.remove() # 删除集合里的所有记录
    for i in range(10):
        db.users.insert({'name':"user" + str(i), 'age':i})
    for u in db.users.find(): print u
    # 显示如下：
    { "_id" : ObjectId("4c47b3372a9b2be866da226e"), "name" : "user0", "age" : 0 }
    { "_id" : ObjectId("4c47b3372a9b2be866da226f"), "name" : "user1", "age" : 1 }
    { "_id" : ObjectId("4c47b3372a9b2be866da2270"), "name" : "user2", "age" : 2 }
    { "_id" : ObjectId("4c47b3372a9b2be866da2271"), "name" : "user3", "age" : 3 }
    { "_id" : ObjectId("4c47b3372a9b2be866da2272"), "name" : "user4", "age" : 4 }
    { "_id" : ObjectId("4c47b3372a9b2be866da2273"), "name" : "user5", "age" : 5 }
    { "_id" : ObjectId("4c47b3372a9b2be866da2274"), "name" : "user6", "age" : 6 }
    { "_id" : ObjectId("4c47b3372a9b2be866da2275"), "name" : "user7", "age" : 7 }
    { "_id" : ObjectId("4c47b3372a9b2be866da2276"), "name" : "user8", "age" : 8 }
    { "_id" : ObjectId("4c47b3372a9b2be866da2277"), "name" : "user9", "age" : 9 }

    for u in db.users.find({"$where":"this.age > 7 || this.age < 3"}): print u
    # 显示如下：
    {u'age': 0.0, u'_id': ObjectId('4c47b3372a9b2be866da226e'), u'name': u'user0'}
    {u'age': 1.0, u'_id': ObjectId('4c47b3372a9b2be866da226f'), u'name': u'user1'}
    {u'age': 2.0, u'_id': ObjectId('4c47b3372a9b2be866da2270'), u'name': u'user2'}
    {u'age': 8.0, u'_id': ObjectId('4c47b3372a9b2be866da2276'), u'name': u'user8'}
    {u'age': 9.0, u'_id': ObjectId('4c47b3372a9b2be866da2277'), u'name': u'user9'}

    for u in db.users.find().where("this.age > 7 || this.age < 3"): print u
    # 显示如下：
    {u'age': 0.0, u'_id': ObjectId('4c47b3372a9b2be866da226e'), u'name': u'user0'}
    {u'age': 1.0, u'_id': ObjectId('4c47b3372a9b2be866da226f'), u'name': u'user1'}
    {u'age': 2.0, u'_id': ObjectId('4c47b3372a9b2be866da2270'), u'name': u'user2'}
    {u'age': 8.0, u'_id': ObjectId('4c47b3372a9b2be866da2276'), u'name': u'user8'}
    {u'age': 9.0, u'_id': ObjectId('4c47b3372a9b2be866da2277'), u'name': u'user9'}

    # 使用自定义的 function, javascript语法的
    for u in db.users.find().where("function() { return this.age > 7 || this.age < 3;}"): print u
    # 显示如下：
    {u'age': 0.0, u'_id': ObjectId('4c47b3372a9b2be866da226e'), u'name': u'user0'}
    {u'age': 1.0, u'_id': ObjectId('4c47b3372a9b2be866da226f'), u'name': u'user1'}
    {u'age': 2.0, u'_id': ObjectId('4c47b3372a9b2be866da2270'), u'name': u'user2'}
    {u'age': 8.0, u'_id': ObjectId('4c47b3372a9b2be866da2276'), u'name': u'user8'}
    {u'age': 9.0, u'_id': ObjectId('4c47b3372a9b2be866da2277'), u'name': u'user9'}

  (11) $exists
    m = db[collName].find({"s": None}).count()
    n = db[collName].find({"s": {'$regex': ".*"}}).count()
    k = db[collName].find({"si": None}).count()
    z = db[collName].find({"si": {'$exists': True}}).count()
