import os
import json
import requests
from pprint import pprint

USERNAME = os.environ.get('SALES_USERNAME')
PASSWORD = os.environ.get('SALES_PASSWORD')
CONSUMER_KEY = os.environ.get('SALES_CLIENT_KEY')
CONSUMER_SECRET = os.environ.get('SALES_CLIENT_SECRET')
DOMAIN_NAME = os.environ.get('SALES_DOMAIN_NAME')

def get_access_token():
    json_data = {
        'grant_type': 'password',
        'username': USERNAME,
        'password': PASSWORD,
        'client_id': CONSUMER_KEY,
        'client_secret': CONSUMER_SECRET,
        'content-type': 'application/json'
    }

    uri_token_request = DOMAIN_NAME + 'services/oauth2/token'
    response = requests.post(uri_token_request, data=json_data)
    return response.json()['access_token']

def post_job(access_token, job_url, job_data):
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-PrettyPrint': '1'
    }

    response = requests.post(job_url, headers=headers, data=json.dumps(job_data).replace('\n', ''))
    return response.json()

def insert_data(access_token, url, data):
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'text/csv',
        'Accept': 'application/json',
        'X-PrettyPrint': '1'
    }

    return requests.put(url, headers=headers, data=data)

def upload_complete(access_token, url):
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json',
        'X-PrettyPrint': '1'
    }
    json_data = {
        'state': 'UploadComplete',
    }

    response = requests.patch(url, headers=headers, json=json_data)
    return response.json()

def check_status(access_token, url):
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Accept': 'application/json',
        'X-PrettyPrint': '1'
    }

    response = requests.get(url, headers=headers)
    return response.json()


access_token = get_access_token()
print(f'ACCESS TOKEN: {access_token}\n')
if not access_token:
    exit(0)

job_data = {
    "object" : "",
    "contentType" : "CSV",
    "operation" : "insert",
    "lineEnding" : "CRLF"
}
job_data['object'] = "Account"

job_url = DOMAIN_NAME + 'services/data/v59.0/jobs/ingest/'
pjr = post_job(access_token, job_url, job_data)
pprint(pjr['contentUrl'])

with open('Account.csv', 'rb') as f:
    data = f.read()
insert_url = DOMAIN_NAME + pjr['contentUrl']
response = insert_data(access_token, insert_url, data)

patch_url = job_url + pjr['id']
completed = upload_complete(access_token, patch_url)

while(True):
    status = check_status(access_token, patch_url)
    pprint(status)

    if (status['state'] != 'InProgress'):
        print('Completed!')
        exit(1)