import json
import os

import boto3

client = boto3.client('ses')


def lambda_handler(event, context):
    print("Got a new User::::::::::::: ", event)
    mailBody = json.loads(event['Records'][0]['body'])
    mail = mailBody['detail']['id']
    print("mail::::: ", mail)
    send_email(mail)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Event triggered Successfully!!",
        }),
    }


def send_email(email):
    ses = boto3.client("ses", region_name="us-west-2")
    ses.send_email(
        Source=os.getenv("SES_FROM_ADDRESS"),
        Destination={"ToAddresses": [email]},
        Message={
            "Body": {
                "Html": {
                    "Charset": "UTF-8",
                    "Data": "<html><body><p>Welcome!!!</p>"
                            f"<h3>You are successfully sign up to our system</h3></body></html>",
                },
            },
            "Subject": {"Charset": "UTF-8", "Data": "Your secret login code"},
        },
    )
