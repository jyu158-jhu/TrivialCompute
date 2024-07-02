import json

import json
# import the AWS SDK (for Python the package name is boto3)
import boto3
import hashlib

import decimal

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select our table
table = dynamodb.Table('Games')

def replace_decimals(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = replace_decimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj

def lambda_handler(event, context):
    print(f"event={event}")
    print(f"context={context}")

    game_id = event['queryStringParameters']['id']
    games = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('id').eq(game_id)
    )
    
    items = games["Items"]
    converted = replace_decimals(items)
    print(f"converted={converted}")

    return {
        "statusCode": 200,
        "body": json.dumps(converted)
    }
