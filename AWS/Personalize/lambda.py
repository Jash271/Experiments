import json
import boto3
def lambda_handler(event, context):
    
    l=[]
    personalize = boto3.client('personalize')
    
    

    personalizeRT = boto3.client('personalize-runtime')
    response = personalizeRT.get_recommendations(
    campaignArn='arn:aws:personalize:us-east-1:474358535128:campaign/recommend-movies',
    userId=event["queryStringParameters"]["name"]
    )
    for item in response['itemList']:
       l.append(item['itemId'])
    return {
        'statusCode': 200,
        
        'body':json.dumps(l),
        
        
    }

