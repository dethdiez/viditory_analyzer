from __future__ import print_function
import httplib2
import os
import io
import six
import time
import json
import hashlib
from subprocess import call
from wand.image import Image

from six.moves import http_client
from apiclient import discovery
from apiclient import http
from apiclient.http import MediaIoBaseDownload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from multiprocessing import Pool as ThreadPool
from multiprocessing import Process

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def DownloadItem(item):
    print('DownloadItem %s'%item['name'])
    request = globalService.files().get_media(fileId=item['id'])
    fh = io.FileIO(item['name'], mode='wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))
    
    name = item['id'] + item['name']
    os.rename(item['name'], name)
    return True


def AnalyzeImage(item):
    name = item['id'] + item['name']
    print('{0} ({1})'.format(name, item['id']))
    with Image(filename=name) as img:
        data = {}
        for k, v in img.metadata.items():
            data[k] = v
        with open ('%s.json'%item['id'], 'w+') as res:
            json.dump(data, res)
    os.remove(name)
    return True


def AnalyzeImages():
    #ищем фотографии на диске (опционально добавить прохождение по дереву)
    results = globalService.files().list(
        q="mimeType contains 'image'", 
        fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No images found.')
    else:
        print('Images:')
        print(len(items))
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id'])) #это потом удалить

    print('')

    
#    results = pool1.map(DownloadItem, items)
    downloader = Process(target = StartDownloadImages, args = (items,))
    downloader.start()
    downloader.join()
    
    analyzer = Process(target = StartAnalyzeImages, args = (items,))
    analyzer.start()
    analyzer.join()


def AnalyzeVideo(item):
    name = item['id'] + item['name']
    jsonName = item['id'] + ".json"
    f = open(jsonName, "w")
    call (["ffprobe","-i",name,"-print_format","json","-show_streams","-show_format","-show_data"], stdout=f)
 
    hasher = hashlib.md5()
    with open(name, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    
    data = '{"md5_hash":%s}'%hasher.hexdigest()
    fp = json.loads(jsonName)
    f = json.dump([data, fp])
    f.close()


def AnalyzeVideos():
    #аналогично с видео
    results = globalService.files().list(
        q="mimeType contains 'video'",
        fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No videos found.')
    else:
        print('Videos') 
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id'])) #тоже удалить

    downloader1 = Process(target = StartDownloadVideos, args = (items,))
    downloader1.start()
    downloader1.join()

    analyzer1 = Process(target = StartAnalyzeVideos, args = (items,))
    analyzer1.start()
    analyzer1.join()


def StartDownloadImages(items):
    print('StartDownload')
    pool1 = ThreadPool(1) # Sets the pool size to 4
    pool1.map(DownloadItem, items)
 #   print(len(downloadedImages))


def StartAnalyzeImages(items):
    print('StartAnalyzeImages')
    pool2 = ThreadPool(1)
    pool2.map(AnalyzeImage, items)


def StartAnalyzeVideos(items):
    print('StartAnalyzeVideos')
    pool3 = ThreadPool(1)
    pool3.map(AnalyzeVideo, items)

def StartDownloadVideos(items):
    print('StartDownload')
    pool4 = ThreadPool(1) # Sets the pool size to 4
    pool4.map(DownloadItem, items)


def StartImageAnalysis(credentials):
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    global globalService
    globalService = service

    AnalyzeImages()

def StartVideoAnalysis(credentials):
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    global globalService
    globalService = service
    AnalyzeVideos()
    
    return True