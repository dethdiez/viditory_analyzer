import pymongo
import json
from pymongo import MongoClient
from bson import json_util
from decimal import Decimal

def StatImages():
	client = MongoClient('mongodb://0.0.0.0:27017/')
	db = client['diplom_mongo_1']
	posts = db.posts
	data = posts.find({"type": "image"})
	data1 = posts.find({"type": "image"})
	count = 0
	weight = 0
	copies = 0
	copiesId = {}
	copiesIdList = []
	imgFormat = {}

	for item in data:		
		count = count + 1
#		print('')
#		print('data:')
#		print(data)
		weight += item['weight']
		keys = []
		for k in item.keys():
			keys.append(k)
		if (imgFormat.get(keys.pop())):
			imgFormat[item['format']] += 1
		else:
			imgFormat[item['format']] = 1
		flag = False
		for item1 in data1:
			if item != item1:
				if (item['md5'] == item1['md5']) and (item1['id'] not in copiesIdList):
					if(flag):
						copies = copies + 1
						copiesId[item['id']].append(item1['id'])
						copiesIdList.append(item1['id'])
					else:
						copies = copies + 2
						copiesId[item['id']] = []
						copiesId[item['id']].append(item1['id'])
						flag = True
						copiesIdList.append(item['id'])
						copiesIdList.append(item1['id'])
	
	maxFormatCount = 0
	maxFormatName = ''
	for k,v in imgFormat.items():
		if v > maxFormatCount:
			maxFormatCount = v
			maxFormatName = k

	stat = {}
	stat['count'] = count
	stat['totalWeight'] = weight
	x = weight/count
	stat['averageWeight'] = round(x,1)
	stat['copiesCount'] = copies
	stat['copies'] = copiesId
	stat['most_popular_img_format'] = maxFormatName

	print('')
#	print(stat)
	return stat

def StatVideos():
	client = MongoClient('mongodb://0.0.0.0:27017/')
	db = client['diplom_mongo_1']
	posts = db.posts
	data = posts.find({"type": "video"})
	data1 = posts.find({"type": "video"})
	count = 0
	fileSize = 0
	copies = 0
	durationMillis = 0
	copiesId = {}
	copiesIdList = []
	videoFormat = {}
	brokenCount = 0
	brokenList = []

	for item in data:		
		count = count + 1
		fileSize += int(item['fileSize'])
		duration += float(item['durationMillis'])
		keys = []
		for k in item.keys():
			keys.append(k)
		if (videoFormat.get(keys.pop())):
			videoFormat[item['extension']] += 1
		else:
			videoFormat[item['extension']] = 1

		if (item['isBroken']):
			brokenCount += 1
			brokenList.append(item['id'])

		flag = False
		for item1 in data1:
			if item['id'] != item1['id']:
				if (item['md5'] == item1['md5']) and (item1['id'] not in copiesIdList):
					if(flag):
						copies = copies + 1
						copiesId[item['id']].append(item1['id'])
						copiesIdList.append(item1['id'])
					else:
						copies = copies + 2
						copiesId[item['id']] = []
						copiesId[item['id']].append(item1['id'])
						flag = True
						copiesIdList.append(item['id'])
						copiesIdList.append(item1['id'])
	
	maxFormatCount = 0
	maxFormatName = ''
	for k,v in imgFormat.items():
		if v > maxFormatCount:
			maxFormatCount = v
			maxFormatName = k

	stat = {}
	stat['count'] = count
	stat['totalSize'] = fileSize
	x = fileSize/count
	stat['averageSize'] = round(x,1)
	stat['totaldurationMillis'] = duration
	stat['averagedurationMillis'] = round((duration/count),6)
	stat['brokenCount'] = brokenCount
	stat['brokenList'] = brokenList
	stat['copiesCount'] = copies
	stat['copies'] = copiesId
	stat['most_popular_video_format'] = maxFormatName

	print('')
#	print(stat)
	return stat

def GetStat():
#	imgStat = StatImages()
	videoStat = StatVideos()
	stat = {"images": imgStat, "videos": videoStat}
	print(stat)

def main():
	StatVideos()

if __name__ == '__main__':
    main()