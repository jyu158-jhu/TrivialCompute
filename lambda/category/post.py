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
    category_id = 'cat_' + hash_string(event['name'].lower())
    category={
        'id': category_id,
        'name': event['name'].lower(),
        'color': event['color'].lower()
    }
    print(f'category={category}')

    existing_category = table.get_item(Key={"id": category_id})
    print(f'existing_category={existing_category}')
    if 'Item' in existing_category:
        response = create_response(existing_category['Item']) 
    else:
        new_category = table.put_item(Item=category,ReturnValues='ALL_OLD')
        print(f'created={new_category}')
        response = create_response(category)
        
    return response


def hash_string(string):
    h = hashlib.new('md5')
    h.update(string.encode())
    return h.hexdigest()

def create_response(item):
    return {
        'id': item['id'],
        'name': item['name'],
        "color": item['color']
    }
