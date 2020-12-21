import pymongo
import json
from bson import ObjectId


mongoclient = pymongo.MongoClient(host="127.0.0.1",port=27017)
MongoDB = mongoclient["table1"]


res = MongoDB.find({})
for el in res:
    print(el)
    el['_id'] = str(el['_id'])
#
# MongoDB.db1.find_one({},{'name':'122fff'})
# MongoDB.db1.find({"_id":0})
#
# res = MongoDB.db1.insert_one({'name':'bbbb', 'age':12})
#
# res = MongoDB.db1.update_one({'name':'bbbb'},{'$set': {'age':12}})
# res = MongoDB.db1.update_many({'name':'bbbb'},{'$set': {'age':12}})
#
# MongoDB.db1.delete_one({'name':'bbbb'})
# MongoDB.db1.delete_many({'name':'bbbb'})
#
# MongoDB.db1.find({}).limit(5).skip(2)
#
# MongoDB.db1.find({}).sort('name', 1)
#
# s = ObjectId('5c3ea77e23652a0218a5ab9a')
#
# res = MongoDB.db1.find_one('_id':s)


results = db.topic_questions.find({'$or': [{'_id':ObjectId('sdgasd')}, {'_id': ObjectId('23k4hh')}]})
for result in results:
    print(result)



from pymongo import UpdateOne,UpdateMany
from pymongo import InsertOne,InsertMany
# 关于UpdateOne和UpdateMany的区别就是，如果查找到多个符合条件的值，
# UpdateOne一次只会更新一条消息，而UpdateMany会一次更新所有符合要求的条目。
requests=[
    UpdateOne({'key':'value1'},{'$set':data1}),
    UpdateOne({'key':'value2'},{'$set':data2}),
    UpdateOne({'_id': 1}, {'$set': {'foo': 'bar'}}),
    ...
    ]
db.collection.bulk_write(requests)
 ———————————————— 
版权声明：本文为CSDN博主「multiangle」的原创文章，遵循CC 4.0 by-sa版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/u014595019/article/details/50918664


db.resume.aggregate([{$sample: {size:100}}])




































