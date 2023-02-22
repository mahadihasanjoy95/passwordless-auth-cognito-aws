import json

import boto3

rds_client = boto3.client('rds-data')

database_name = "products"
db_cluster_arn = "arn:aws:rds:ap-northeast-1:534678543881:cluster:passless-solution-rdscluster-vgym39evltzw"
db_credentials_secrets_arn = "arn:aws:secretsmanager:ap-northeast-1:534678543881:secret:DBSecret-Swhk4V"


def lambda_handler(event, context):
    sql = "select * from Persons;"

    response = rds_client.execute_statement(
        secretArn=db_credentials_secrets_arn,
        database=database_name,
        resourceArn=db_cluster_arn,
        sql=sql
    )
    print("RESPONSE:::::::::::: ", response)

    return {"statusCode": 200,
            'body': json.dumps(response["records"]),
            # "location": ip.text.replace("\n", "")

            }
