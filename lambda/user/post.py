import json
# import the AWS SDK (for Python the package name is boto3)
import boto3
import hashlib

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select our table
table = dynamodb.Table('UserDB')

def lambda_handler(event, context):
    user_id = 'user_' + hash_string(event['username'])
    user={
        'user_id': user_id,
        'username': event['username'],
        'password': hash_string(event['password']),
        "email": event['email']
    }
    print(f'user={user}')

    existing_user = table.get_item(Key={"user_id": user_id})
    print(f'existing_user={existing_user}')
    if 'Item' in existing_user:
        response = create_response(existing_user['Item']) 
    else:
        new_user = table.put_item(Item=user,ReturnValues='ALL_OLD')
        print(f'created={new_user}')
        response = create_response(user)
        
    return response


def hash_string(string):
    h = hashlib.new('md5')
    h.update(string.encode())
    return h.hexdigest()

def create_response(item):
    return {
        'user_id': item['user_id'],
        'username': item['username'],
        "email": item['email']
    }
