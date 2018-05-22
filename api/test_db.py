import pymongo
from pymongo import MongoClient
import json
from bson import json_util


client = MongoClient('mongodb://0.0.0.0:27017/')
db = client['diplom_mongo_1']

#post = {"author": "Yury", "text": "test post", "tags": ["mongoDB","python"]}
jsonFile = open("example.json", "r")
data = json_util.loads(jsonFile.read())
posts = db.posts
post_id = posts.insert(data, check_keys=False)
cursor = posts.find({})
for document in cursor: 
	print(document)
posts.delete_many({})

def CleanDB():
	client = MongoClient('mongodb://0.0.0.0:27017/')
	db = client['diplom_mongo_1']
	posts = db.posts
	posts.delete_many({})

def InsertDoc(name):
	print('start insert %s'%name)
	client = MongoClient('mongodb://0.0.0.0:27017/')
	db = client['diplom_mongo_1']

	#post = {"author": "Yury", "text": "test post", "tags": ["mongoDB","python"]}
	jsonFile = open(name, "r")
	data = json_util.loads(jsonFile.read())
	posts = db.posts
	post_id = posts.insert(data, check_keys=False)
#	cursor = posts.find({})
#	for document in cursor: 
#		print(document)