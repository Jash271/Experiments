import json
import boto3


def lambda_handler(event, context):

    message = "Hello There!"
    client = boto3.client('sns')
    response = client.publish(
        TargetArn='arn:aws:sns:us-east-1:474358535128:Demo-Notification',
        Message=json.dumps({'default': json.dumps(message),
                            'sms': 'here a short version of the message',
                            'email': 'here a longer version of the message'}),
        Subject='a short subject for your message',
        MessageStructure='json'
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Message Sent!')
    }
