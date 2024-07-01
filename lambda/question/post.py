import json

import json
# import the AWS SDK (for Python the package name is boto3)
import boto3
import hashlib

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select our table
table = dynamodb.Table('Questions')


# {
#   "category_name": "string",
#   "question_text": "string",
#   "answer": "string",
#   "media_url": "string",
#   "difficulty": "string"
# }

def lambda_handler(event, context):
    print(f"event={event}")
    print(f"context={context}")
    
    request_body = json.loads(event['body'])
    
    question_id = 'que_' + hash_string(request_body['question_text'].lower())
    question={
        'id': question_id,
        'category_name': request_body['category_name'],
        'question_text': request_body['question_text'],
        'media_url': request_body['media_url'],
        'difficulty': request_body['difficulty'],
        'answer': request_body['answer'].lower()
    }
    print(f'question={question}')

    existing_question = table.get_item(Key={"id": question_id})
    print(f'existing_question={existing_question}')
    if 'Item' in existing_question:
        body = create_body(existing_question['Item']) 
    else:
        new_question = table.put_item(Item=question,ReturnValues='ALL_OLD')
        print(f'created={new_question}')
        body = create_body(question)
        
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }


def hash_string(string):
    h = hashlib.new('md5')
    h.update(string.encode())
    return h.hexdigest()

# {
#   "id": "string",
#   "category_name": "string",
#   "question_text": "string",
#   "answer": "string",
#   "media_url": "string",
#   "difficulty": "string"
# }
def create_body(item):
    return {
        'id': item['id'],
        'category_name': item['category_name'],
        'answer': item['answer'],
        'media_url': item['media_url'],
        'difficulty': item['difficulty'],
        "question_text": item['question_text']
    }
