import pymongo
from pymongo import MongoClient
import json
from bson import json_util


client = MongoClient('localhost', 27017)
db = client.test_database

#post = {"author": "Yury", "text": "test post", "tags": ["mongoDB","python"]}
jsonFile = open("example.json", "r")
data = json_util.loads(jsonFile.read())
posts = db.posts
post_id = posts.insert_one(data).inserted_id
cursor = posts.find({})
for document in cursor: 
	print(document)