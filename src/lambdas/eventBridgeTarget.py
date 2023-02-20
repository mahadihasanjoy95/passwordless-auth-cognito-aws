import json


def lambda_handler(event, context):
    print("Got an event::::::::::::: ", event)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Event triggered Successfully!!",
        }),
    }
