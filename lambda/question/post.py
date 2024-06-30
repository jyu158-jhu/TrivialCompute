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
    question_id = 'que_' + hash_string(event['question_text'].lower())
    question={
        'id': question_id,
        'category_name': event['category_name'],
        'question_text': event['question_text'],
        'media_url': event['media_url'],
        'difficulty': event['difficulty'],
        'answer': event['answer'].lower()
    }
    print(f'question={question}')

    existing_question = table.get_item(Key={"id": question_id})
    print(f'existing_question={existing_question}')
    if 'Item' in existing_question:
        response = create_response(existing_question['Item']) 
    else:
        new_question = table.put_item(Item=question,ReturnValues='ALL_OLD')
        print(f'created={new_question}')
        response = create_response(question)
        
    return response


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
def create_response(item):
    return {
        'id': item['id'],
        'category_name': item['category_name'],
        'answer': item['answer'],
        'media_url': item['media_url'],
        'difficulty': item['difficulty'],
        "question_text": item['question_text']
    }
