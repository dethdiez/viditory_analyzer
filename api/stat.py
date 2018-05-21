import pymongo
import json
from pymongo import MongoClient
from bson import json_util

def StatImages():
	client = MongoClient('mongodb://0.0.0.0:27017/')
	db = client['diplom_mongo_1']
	posts = db.posts
	data = posts.find({"type": "image"})
	count = 0
	weight = 0
	copies = 0
	copiesId = {}
	copiesIdList = []
	imgFormat = {}
	for item in data:
		count += 1
		weight += item['weight']
		if (imgFormat.get(item)):
			imgFormat[item['format']] += 1
		else:
			imgFormat[item['format']] = 1
		flag = False
		for item1 in data:
			if item != item1:
				if (item['md5'] == item1['md5']) and (item1['id'] not in copiesIdList):
					if(flag):
						copies += 1
						copiesId[item['id']].append(item1['id'])
						copiesIdList.append(item1['id'])
					else:
						copies += 2
						copiesId[item['id']] = []
						copiesId[item['id']].append(item1['id'])
						flag = True
						copiesIdList.append(item['id'])
						copiesIdList.append(item1['id'])
	print(copiesIdList)