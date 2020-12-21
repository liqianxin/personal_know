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


# 聚合
import pymongo
import json
from bson import ObjectId

mongoclient = pymongo.MongoClient(host="mongodb1.dev.zippia.com",port=27017)
MongoDB = mongoclient["zippia"]

pipeline = [
    {'$match' : {}},
    {'$group':{'_id':'$lay_title','counts':{'$sum':1}}},
    {'$sort' :{'counts': -1}},
    # {'$limit':20}
]
for i in MongoDB.skill_master.aggregate(pipeline):
    print(i)





sql:
db.title.aggregate([{$project: {size: {$size: "$the_list"}}}, {$group: {_id: "C", avg: {$avg: "$size"}, max: {$max: "$size"}}}])






####################################################################################

db.sales.insertMany([
  { "_id" : 1, "item" : "abc", "price" : NumberDecimal("10"), "quantity" : NumberInt("2"), "date" : ISODate("2014-03-01T08:00:00Z") },
  { "_id" : 2, "item" : "jkl", "price" : NumberDecimal("20"), "quantity" : NumberInt("1"), "date" : ISODate("2014-03-01T09:00:00Z") },
  { "_id" : 3, "item" : "xyz", "price" : NumberDecimal("5"), "quantity" : NumberInt( "10"), "date" : ISODate("2014-03-15T09:00:00Z") },
  { "_id" : 4, "item" : "xyz", "price" : NumberDecimal("5"), "quantity" :  NumberInt("20") , "date" : ISODate("2014-04-04T11:21:39.736Z") },
  { "_id" : 5, "item" : "abc", "price" : NumberDecimal("10"), "quantity" : NumberInt("10") , "date" : ISODate("2014-04-04T21:23:13.331Z") },
  { "_id" : 6, "item" : "def", "price" : NumberDecimal("7.5"), "quantity": NumberInt("5" ) , "date" : ISODate("2015-06-04T05:08:13Z") },
  { "_id" : 7, "item" : "def", "price" : NumberDecimal("7.5"), "quantity": NumberInt("10") , "date" : ISODate("2015-09-10T08:43:00Z") },
  { "_id" : 8, "item" : "abc", "price" : NumberDecimal("10"), "quantity" : NumberInt("5" ) , "date" : ISODate("2016-02-06T20:20:13Z") },
])


db.sales.aggregate( [
  {
    $group: {
       _id: null,
       count: { $sum: 1 }
    }
  }
] )
{ "_id" : null, "count" : 8 }

-----------------------------------------------------------------------------------
db.sales.aggregate( [ { $group : { _id : "$item" } } ] )
{ "_id" : "abc" }
{ "_id" : "jkl" }
{ "_id" : "def" }
{ "_id" : "xyz" }

####################################################################################

























