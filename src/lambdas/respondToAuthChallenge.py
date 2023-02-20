import json
import os

import boto3

cognito_client = boto3.client('cognito-idp')
client_id = os.getenv('UserPoolClient')


def lambda_handler(event, context):
    """Respond To Auth Challenge

    """
    print(event, "-------Start------------")
    body = json.loads(event['body'])
    challenge = body.get('challenge')
    email = body.get('email')
    session = body.get('session')
    answer = body.get('answer')

    response = cognito_client.respond_to_auth_challenge(
        ClientId=client_id,
        ChallengeName=challenge,
        Session=session,
        ChallengeResponses={
            'USERNAME': email,
            'ANSWER': answer
        }
    )
    print("Response:::::::::::: ", response)
    return {
        "statusCode": 200,
        "headers": {},
        'body': json.dumps(response, indent=4, sort_keys=True, default=str),  # default=decimal_default),
    }
