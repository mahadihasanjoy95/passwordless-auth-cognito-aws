import json
import os
import random

import boto3
import datetime
from botocore.exceptions import ClientError

client = boto3.client('cognito-idp')

UserPool = os.getenv('UserPool')
client_id = os.getenv('UserPoolClient')
event_client = boto3.client('events')

lower = "abcdefghijklmnopqrstuvwxyz"
upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"
symbols = "@#$&_-()=%*:/!?+."


def lambda_handler(message, context):
    if ('body' not in message or
            message['httpMethod'] != 'POST'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }

    user = json.loads(message['body'])

    try:
        allString = lower + upper + numbers + symbols
        length = 11
        password = "".join(random.sample(allString, length))
        response = client.sign_up(
            ClientId=client_id,
            Username=user['email'],
            Password=password,
            UserAttributes=[{'Name': 'email',
                             'Value': user['email']}],
        )
        eventResponse = event_client.put_events(Entries=[
            {
                "Detail": json.dumps({
                    "state": "created",
                    "id": user['email']
                }),
                "DetailType": 'New User',
                "Source": 'demo.users',
                "Time": datetime.datetime.now()
            }
        ])
        return {
            "statusCode": 200,
            "headers": {},
            'body': json.dumps(response, indent=4, sort_keys=True, default=str),  # default=decimal_default),
        }
    except ClientError as err:
        # Probably user already exists
        print("ERROR:::::::::::: ", err)
        return {
            "statusCode": 502,
            "headers": {},
            'body': json.dumps({'msg': 'Bad Request'})
        }
