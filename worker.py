import environment
import policy
import jwt

from model import Entry
from model import db
from datetime import datetime


def auth(event, context):
    if event.get("source") in ["aws.events", "serverless-plugin-warmup"]:
        return {}

    claims = None
    try:
        token = event['authorizationToken'][7:]
        claims = jwt.decode(token, 'secret', algorithm='HS256')
    except Exception as err:
        print(f'Unauthorized - {err}')
        raise Exception('Unauthorized')
    else:
        principalId = claims['subject']

        tmp = event['methodArn'].split(':')
        apiGatewayArnTmp = tmp[5].split('/')
        awsAccountId = tmp[4]

        document = policy.AuthPolicy(principalId, awsAccountId)
        document.restApiId = apiGatewayArnTmp[0]
        document.region = tmp[3]
        document.stage = apiGatewayArnTmp[1]
        document.allowAllMethods()

        # Finally, build the policy
        authResponse = document.build()

        # Attach decoded + verified claims
        authResponse['context'] = claims

        return authResponse


def worker(event, context):
    """Handler for processing batch event to database ingestion"""
    if event.get("source") in ["aws.events", "serverless-plugin-warmup"]:
        return {}

    for record in event['Records']:
        timestamp = float(record['attributes']['SentTimestamp']) / 1000
        body = record['body']
        hash_key = record['md5OfBody']
        entry = Entry(created_at=datetime.fromtimestamp(
            timestamp), content=body, hash_key=hash_key)
        db.session.add(entry)
    else:
        db.session.commit()
    return None
