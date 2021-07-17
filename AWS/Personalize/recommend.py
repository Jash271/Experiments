import boto3
personalize = boto3.client('personalize')
repsonse = personalize.list_recipes()


personalizeRT = boto3.client('personalize-runtime')
response = personalizeRT.get_recommendations(
    campaignArn='arn:aws:personalize:us-east-1:474358535128:campaign/recommend-movies',
    userId='6'
)
for item in response['itemList']:
    print(item['itemId'])
