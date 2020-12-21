import pymongo
import json
from bson import ObjectId

mongoclient = pymongo.MongoClient(host="127.0.0.1",port=27017)
MongoDB = mongoclient["locals"]

# res = MongoDB.user.find({})
# for i in res:
#     print(i)
#     i["_id"] = str(i.get("_id"))
#     print(i.get("_id"),type(i.get("_id")))
#     s = json.dumps(i)

# res = MongoDB.user.find_one({},{"_id":0})
# print(res)
# res = list(MongoDB.user.find({"id":1}))
# print(res)

#增加
# res = MongoDB.user.insert_one({"id":1,"age":55,"name":"taibai"})
# print(res,type(res),res.inserted_id)

# res = MongoDB.user.insert_many([{"id":1,"age":55,"name":"taibai"},{"id":1,"age":55,"name":"taibai"}])
# print(res,type(res),res.inserted_ids)

# 修改：
# res = MongoDB.user.update_one({"age":55},{"$set":{"name":"四金"}})
# print(res,dir(res))

# MongoDB.user.update_many({"age":55},{"$set":{"name":"四金"}})
db['dataframe'].delete_many({"_id": {"$gte": 1582300020}})

#删除：
# res = MongoDB.user.delete_one({"id":1})
# res = MongoDB.user.delete_many({"id":1})


# sort limit skip

# res = list(MongoDB.user.find({}).limit(5).skip(2))
# print(res)

# res = list(MongoDB.user.find({}).sort("age",pymongo.DESCENDING).limit(5).skip(2))
# print(res)

# s = ObjectId("5c3ea77e23652a0218a5ab9a")
#
# res = MongoDB.user.find_one({"_id":ObjectId("5c3ea77e23652a0218a5ab9a")})
# print(res)


# u:今天天气怎么样 a:你要查询哪所城市 u:北京 a:天气
# { '_id': ObjectId('5c3ea77e23652a0218a5ab9a')
#   chat_list:[
#   { user:今天天气怎么样,a:你要查询哪所城市},
#   {u:北京 ,a:天气}
# ]
# }


# 扩展内容 - 查询聊天记录



