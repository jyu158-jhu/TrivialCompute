import json

import json
# import the AWS SDK (for Python the package name is boto3)
import boto3
import hashlib

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select our table
table = dynamodb.Table('Questions')

def lambda_handler(event, context):
    print(f"event={event}")
    print(f"context={context}")

    category_name = event['queryStringParameters']['category']
    questions = table.query(
        IndexName="category_name-index",
        KeyConditionExpression=boto3.dynamodb.conditions.Key('category_name').eq(category_name)
    )
    
    print(f"questions={questions}")

    return {
        "statusCode": 200,
        "body": json.dumps(questions["Items"])
    }
