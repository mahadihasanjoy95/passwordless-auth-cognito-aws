import os
import secrets
from string import digits

import boto3

client = boto3.client('ses')
secretLoginCode = ""


def lambda_handler(event, context):
    """Create Challenge and then Send Notification
    """
    rand = secrets.SystemRandom()
    print(event, '-------------- start ---------------')

    response = event.get('response')
    request = event.get('request')
    print("Request:::::: ", request)
    session = request.get('session')
    print("Email:::::: ", event["request"]["userAttributes"]["email"])

    if (not session) or len(session) == 0:
        print(event, '--------create Challenge-------------')
        secret_login_code = "".join(rand.choice(digits) for _ in range(6))
        send_email(event["request"]["userAttributes"]["email"], secret_login_code)
    else:
        print(event, '--------Used existing Challenge-------------')
        previousChallenge = session[0]
        secret_login_code = previousChallenge.get('challengeMetadata')

    response.update({
        'privateChallengeParameters': {'answer': secret_login_code},
        'challengeMetadata': secretLoginCode,
        'publicChallengeParameters': {
            'answer': secretLoginCode
        }
    })

    print(event, '--------end-------------')

    return event


def send_email(email, code):
    ses = boto3.client("ses", region_name="us-west-2")
    ses.send_email(
        Source=os.getenv("SES_FROM_ADDRESS"),
        Destination={"ToAddresses": [email]},
        Message={
            "Body": {
                "Html": {
                    "Charset": "UTF-8",
                    "Data": "<html><body><p>This is your secret login code:</p>"
                            f"<h3>{code}</h3></body></html>",
                },
                "Text": {"Charset": "UTF-8", "Data": f"Your secret login code: {code}"},
            },
            "Subject": {"Charset": "UTF-8", "Data": "Your secret login code"},
        },
    )
