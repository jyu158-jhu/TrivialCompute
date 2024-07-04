import json

import json
# import the AWS SDK (for Python the package name is boto3)
import boto3
import hashlib

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select our table
table = dynamodb.Table('Questions')


def hash_string(string):
    h = hashlib.new('md5')
    h.update(string.encode())
    return h.hexdigest()

# [ 
#   {
#     "category_name": "string",
#     "question_text": "string",
#     "answer": "string",
#     "media_url": "string",
#     "difficulty": "string"
#   }
# ]
def lambda_handler(event, context):
    print(f"event={event}")
    print(f"context={context}")
    
    request_body = json.loads(event['body'])
    questions = []
    for item in request_body:
        question_id = 'que_' + hash_string(item['question_text'].lower())
        question={
            'id': question_id,
            'category_name': item['category_name'],
            'question_text': item['question_text'],
            'media_url': item['media_url'],
            'answer': item['answer'].lower()
        }
        print(f'question={question}')
        table.put_item(Item=question)
        questions.append(question)

    return {
        'statusCode': 200,
        'body': json.dumps(questions)
    }
