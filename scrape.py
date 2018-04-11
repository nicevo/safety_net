import datetime
import json
import os
import random
import requests
import time
from pprint import pprint
from googleapiclient import discovery


def request_until_succeed(url):
    success = False
    while success is False:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                success = True
            else:
                print('\n{}: status {} for URL {}, retrying in 5s'.format(datetime.datetime.now(), response.status_code,
                                                                          url))
                time.sleep(5)
        except Exception as e:
            print('\n{}: error for URL {}: {}, retrying in 5s'.format(datetime.datetime.now(), url, e))
            time.sleep(5)

    return response.text


def getFacebookPageFeedData(page_id, msg_limit, access_token):
    # construct the URL string from template
    url_template = ('https://graph.facebook.com/{}/feed/?fields=message,link,created_time,type,name,id,'
                    'likes.limit(1).summary(true),comments.limit(1).summary(true),shares&'
                    'limit={}&access_token={}')
    url = url_template.format(page_id, msg_limit, access_token)
    # retrieve data
    data = json.loads(request_until_succeed(url))
    return data


def analyzeToxicity(text, key):
    # Generates API client object dynamically based on service name and version.
    service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=key)
    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }
    response = service.comments().analyze(body=analyze_request).execute()
    #pprint(response)
    return response['attributeScores']['TOXICITY']['summaryScore']['value']


def analize(feed_data, key):
    sum = 0
    count = 0;
    result = {}
    result["messages"] = []
    for m in feed_data:
        subresult = {}
        subresult["message"] = m['message']
        subresult["likes"] = m['likes']['summary']['total_count']
        subresult["shares"] = m['shares']['count']
        subresult["toxicity"] = analyzeToxicity(m['message'], key)
        sum += subresult["toxicity"]
        count += 1;
        result["messages"].append(subresult)
    result["average_score"] = sum / count
    return result


def process(page_id='nytimes', msgcount=2):
    try:
        app_id = os.environ['FB_APP_ID']
        app_secret = os.environ['FB_APP_SECRET']
        key = os.environ['PERSPECTIVE_API_KEY']
    except KeyError as e:
        return {
            "statusCode": 500,
            "body": 'ERROR: Please define environment variables PERSPECTIVE_API_KEY, FB_APP_ID and FB_APP_SECRET.'
        }

    access_token = app_id + '|' + app_secret

    feed_data = getFacebookPageFeedData(page_id, msgcount, access_token)['data']
    result = analize(feed_data, key)

    body = {
        "page": page_id,
        "msgcount": msgcount,
        "verdict": result
    }
    return body


def endpoint(event, context):
    page_id = 'nytimes'
    if 'page' in event['queryStringParameters']:
        page_id = event['queryStringParameters']['page']

    msgcount = 2
    if 'msgcount' in event['queryStringParameters']:
        msgcount = (int)(event['queryStringParameters']['msgcount'])
    if msgcount > 100:
        msgcount = 100

    body = process(page_id, msgcount)

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


if __name__ == '__main__':
    pprint(process("natgeo",3))
