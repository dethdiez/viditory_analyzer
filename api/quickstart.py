from __future__ import print_function
import httplib2
import os
import io
import six
import statistics
import time

import pdb

from six.moves import http_client
from googleapiclient import discovery
from googleapiclient import http
from googleapiclient.http import MediaIoBaseDownload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from analyzer import StartImageAnalysis, StartVideoAnalysis
from test_db import CleanDB

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES = 'https://www.googleapis.com/auth/drive' 
CLIENT_SECRET_FILE = 'client_secret_all_cred.json' 
APPLICATION_NAME = 'Drive API Python Quickstart' 


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~') 
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

def start(owner):
	start_time = time.time()
    main(owner)
    print ('algorithm running time:')
    print ('-- %s seconds --'%(time.time() - start_time))

def test():
    return True

def main(owner):
    credentials = get_credentials()
#    owner = "sova@auditory.ru"
    CleanDB();
#    pdb.set_trace()
#    StartImageAnalysis(credentials, owner)
    StartVideoAnalysis(credentials, owner)
    statistics.GetStat()
#    credentials = get_new_credentials()
"""    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    
    results = service.files().list(
        q="mimeType contains 'image'", 
        fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No images found.')
    else:
        print('Images:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id'])) 

    
    for item in items:
        request = service.files().get_media(fileId=item['id'])
        fh = io.FileIO(item['name'], mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print ("Download %d%%." % int(status.progress() * 100))

    print('')

    
    results = service.files().list(
        q="mimeType contains 'video'",
        fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No videos found.')
    else:
        print('Videos') 
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id'])) 

    
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
    main(arg1)