import json

import json
# import the AWS SDK (for Python the package name is boto3)
import boto3
import hashlib

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select our table
table = dynamodb.Table('Categories')

def lambda_handler(event, context):
    print(f"event={event}")
    print(f"context={context}")

    scan_kwargs = {
        "Limit": 10
    }
    categories = table.scan(**scan_kwargs)
    print(f"categories={categories}")

    return {
        "statusCode": 200,
        "body": json.dumps(categories['Items'])
    }
