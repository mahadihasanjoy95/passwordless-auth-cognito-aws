import json
import os

import sqlalchemy

cluster_arn = os.getenv('DbCluster')
secret_arn = os.getenv('DbSecret')


def lambda_handler(event, context):
    engine = sqlalchemy.create_engine('mysql://:@/products',
                                      echo=True,
                                      connect_args=dict(aurora_cluster_arn=cluster_arn, secret_arn=secret_arn))

    with engine.connect() as conn:
        for result in conn.execute("select * from Persons"):
            print(result)
            return {"statusCode": 200,
                    'body': json.dumps(result["records"]),
                    }
