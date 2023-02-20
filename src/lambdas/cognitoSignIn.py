import json
import os
import random

import boto3

USER_PASS_AUTH_FLOW = 'USER_PASSWORD_AUTH'
CUSTOM_AUTH_FLOW = 'CUSTOM_AUTH'
REFRESH_TOKEN = 'REFRESH_TOKEN'
cognito_client = boto3.client('cognito-idp')
client_id = os.getenv('UserPoolClient')

lower = "abcdefghijklmnopqrstuvwxyz"
upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"
symbols = "@#$&_-()=%*:/!?+."


def sign_me_in(contact, password):
    """SignIn
    """
    try:
        response = cognito_client.initiate_auth(
            ClientId=client_id,
            AuthFlow='CUSTOM_AUTH',
            AuthParameters={
                'USERNAME': contact,
                'PASSWORD': password
            }
        )

    except cognito_client.exceptions.NotAuthorizedException:
        return None, "The username or password is incorrect"
    except Exception as e:
        print(e, '------------------ signin error  ---------------------')
        return None, "Unknown error"
    return response, None


def lambda_handler(event, context):
    if ('body' not in event or
            event['httpMethod'] != 'POST'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }
    body = json.loads(event['body'])
    contact = body.get('email')
    allString = lower + upper + numbers + symbols
    length = 11
    password = "".join(random.sample(allString, length))
    print("Here Is Your Password:", password)
    response, error = sign_me_in(contact, password)
    if error:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "detail": error,
            }),
        }
    return {
        "statusCode": 200,
        "body": json.dumps({
            "detail": response,
        }),
    }
