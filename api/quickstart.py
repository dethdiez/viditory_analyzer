from __future__ import print_function
import httplib2
import os
import io
import six

import pdb

from six.moves import http_client
from apiclient import discovery
from apiclient import http
from apiclient.http import MediaIoBaseDownload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from analyzer import StartImageAnalysis, StartVideoAnalysis

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

#Данные для авторизации
SCOPES = 'https://www.googleapis.com/auth/drive' #права
CLIENT_SECRET_FILE = 'client_secret_all_cred.json' #клиентский файл с данными для доступа
APPLICATION_NAME = 'Drive API Python Quickstart' #имя проекта (указал дефолтное)


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~') #здесь опционально вставить доступ к рандомной директории (попросить пользователя открыть доступ к директории по ссылке)
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_new_credentials():
    home_dir = os.path.expanduser('/app')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    if flags:
        credentials = tools.run_flow(flow, store, flags)
    else: # Needed only for compatibility with Python 2.6
        credentials = tools.run(flow, store)
    print('Storing credentials to ' + credential_path)
    return credentials

def start():
    main()

def main():
    credentials = get_credentials()
#    pdb.set_trace()
#    StartImageAnalysis(credentials)
    StartVideoAnalysis(credentials)
#    credentials = get_new_credentials()
"""    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    #ищем фотографии на диске (опционально добавить прохождение по дереву)
    results = service.files().list(
        q="mimeType contains 'image'", 
        fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No images found.')
    else:
        print('Images:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id'])) #это потом удалить

    #выкачиваем найденные файлы (после закачки сразу отправить на анализ, после удалить)
    for item in items:
        request = service.files().get_media(fileId=item['id'])
        fh = io.FileIO(item['name'], mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print ("Download %d%%." % int(status.progress() * 100))

    print('')

    #аналогично с видео
    results = service.files().list(
        q="mimeType contains 'video'",
        fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No videos found.')
    else:
        print('Videos') 
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id'])) #тоже удалить

    #выкачиваем найденные файлы (после закачки сразу отправить на анализ, после удалить)
    for item in items:
        request = service.files().get_media(fileId=item['id'])
        fh = io.FileIO(item['name'], mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print ("Download %d%%." % int(status.progress() * 100))

    print('') """

if __name__ == '__main__':
    main()