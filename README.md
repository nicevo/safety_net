# SafetyNet

## Summary
The product is intended for retrieving pages from facebook given a page
name and rating the resulting dataset for toxicity. To access facebook
pages, set environement variables `FB_APP_ID`, `FB_APP_SECRET` to the
app_id and app_secret respectively.

## Prerequisites
Python3
Install requirements by running (only for local run):
```
pip3 install -r requirements.txt
```

Install serverless
```
brew install node
npm install -g serverless
```

Python requirements plugin for serverless
```
npm install --save serverless-python-requirements
```

AWS cli
```
brew install awscli
```

Configure secrets
```
aws ssm put-parameter --name fbAppId --type String --value XXXXXXXXXX --profile serverless --region us-east-1
aws ssm put-parameter --name fbAppSecret --type String --value XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX --profile serverless --region us-east-1
```

## How to run
Run in console/terminal/shell:
```
FB_APP_ID=XXXXXXXXXX FB_APP_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX python3 scrape.py
```

## Deploy and test

run
```
 sls deploy
```

go to: https://XXXXXXXX.execute-api.us-east-1.amazonaws.com/stg/?page=natgeo&msgcount=500

Note: messages capped to 100

## Inspiration

Page scraping for facebook
http://minimaxir.com/2015/07/facebook-scraper/
https://github.com/minimaxir/facebook-page-post-scraper/blob/master/examples/how_to_build_facebook_scraper.ipynb

Perspective API 
https://www.perspectiveapi.com 
https://github.com/conversationai/perspectiveapi/blob/master/quickstart.md 

## ToDo

- pass dataset through api
- provide stats
- make online version
- grab wow etc ...

## Troubleshoot

see logs
```
sls logs --function safetyNet -t
```

use specific profile
```
sls deploy -v --stage stg --aws-profile [my-awesome-profile]
```
 
deploy with debug on
```
SLS_DEBUG=* sls deploy -v --stage stg --aws-profile serverless
```

 
