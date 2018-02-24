

# import some Python dependencies

import urllib2
import json
import datetime
import csv
import time




# Since the code output in this notebook leaks the app_secret,
# it has been reset by the time you read this.

app_id = ""
app_secret = "" # DO NOT SHARE WITH ANYONE!

access_token = app_id + "|" + app_secret

page_id = 'nytimes'

def testFacebookPageData(page_id, access_token):
    
    # construct the URL string
    base = "https://graph.facebook.com/v2.4"
    node = "/" + page_id
    parameters = "/?access_token=%s" % access_token
    url = base + node + parameters
    
    # retrieve data
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data = json.loads(response.read())
    
    print json.dumps(data, indent=4, sort_keys=True)
    

testFacebookPageData(page_id, access_token)



def request_until_succeed(url):
    req = urllib2.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception, e:
            print e
            time.sleep(5)
            
            print "Error for URL %s: %s" % (url, datetime.datetime.now())

    return response.read()


