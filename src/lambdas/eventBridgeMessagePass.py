import datetime
import json

import boto3

client = boto3.client('events')


def lambda_handler(event, context):
    response = client.put_events(Entries=[
        {
            "Detail": json.dumps({
                "state": "created",
                "id": "123"
            }),
            "DetailType": 'New order',
            "Source": 'demo.orders',
            "Time": datetime.datetime.now()
        }
    ])

    print("RESPONSE OF TRIGGERING:::: ", response)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": response,
        }),
    }
