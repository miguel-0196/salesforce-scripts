import os
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

    uri_token_request = DOMAIN_NAME + '/services/oauth2/token'
    response = requests.post(uri_token_request, data=json_data)
    return response.json()['access_token']


def get_data(access_token, url):
    # Getting Org API Usage Detail
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get(url, headers=headers)

    # Extract the data from the response
    return response.json()


url = 'http://d1u000000rqgauae-dev-ed.my.salesforce.com/services/data/v59.0/query/?q=SELECT+Id,Name+FROM+Quote'
access_token = get_access_token()
print(f'ACCESS TOKEN: {access_token}\n')
if not access_token:
    exit(0)

data = get_data(access_token, url)
pprint(data)