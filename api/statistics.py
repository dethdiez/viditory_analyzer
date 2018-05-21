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
	weight = 0
	copies = 0
	duration = 0
	duration_ts = 0
	copiesId = {}
	copiesIdList = []
	imgFormat = {}

	for item in data:		
		count = count + 1
		weight += int(item['format']['size'])
		duration += float(item['streams'].pop().get('duration'))
		duration_ts += int(item['streams'].pop().get('duration_ts'))
		keys = []
		for k in item.keys():
			keys.append(k)
		if (imgFormat.get(keys.pop())):
			imgFormat[item['extension']] += 1
		else:
			imgFormat[item['extension']] = 1
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
	stat['totalWeight'] = weight
	x = weight/count
	stat['averageWeight'] = round(x,1)
	stat['totalDuration'] = duration
	stat['averageDuration'] = round((duration/count),6)
	stat['totalDuration_ts'] = duration_ts
	stat['averageDuration_ts'] = round((duration_ts/count),1)
	stat['copiesCount'] = copies
	stat['copies'] = copiesId
	stat['most_popular_video_format'] = maxFormatName

	print('')
#	print(stat)
	return stat

def GetStat():
	imgStat = StatImages()
	videoStat = StatVideos()
	stat = {"images": imgStat, "videos": videoStat}
	print(stat)

def main():
	StatVideos()

if __name__ == '__main__':
    main()