
import boto3

cognito_client = boto3.client('cognito-idp')


def lambda_handler(event, context):
    """Verify Auth Challenge

    """
    print(event, '--------- Start --------------')

    response = event.get('response')
    request = event.get('request')
    # session = request.get('session')

    answerCorrect = False

    expectedAnswer = request.get('privateChallengeParameters').get('answer')
    challengeAnswer = request.get('challengeAnswer')

    if challengeAnswer == expectedAnswer:
        answerCorrect = True
        pool_id = event.get('userPoolId')
        userName = event.get('userName')

        # Update user Attributes
        result = cognito_client.admin_update_user_attributes(
            UserPoolId=pool_id,
            Username=userName,
            UserAttributes=[
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                },
            ]
        )

    response.update({
        'answerCorrect': answerCorrect
    })

    print(event, "-----end---------")

    return event
