import json

# import the AWS SDK (for Python the package name is boto3)
import boto3
import hashlib
import time
import decimal

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select our table
table_game = dynamodb.Table('Games')
table_category = dynamodb.Table('Categories')
table_question = dynamodb.Table('Questions')
table_player = dynamodb.Table('Players')

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

def get_categories():
    scan_kwargs = {
        "Limit": 4
    }    
    categories = table_category.scan(**scan_kwargs)
    print(f"categories={categories}")
    return categories['Items']


def get_questions(category_name):
    questions = table_question.query(
        IndexName="category_name-index",
        KeyConditionExpression=boto3.dynamodb.conditions.Key('category_name').eq(category_name),
        Limit=4
    )
    
    # print(f"category={category_name}, questions={questions}")
    return questions['Items']
    
    
def hash_string(string):
    h = hashlib.new('md5')
    h.update(string.encode())
    return h.hexdigest()

# {
#   "player_id": "string",
#   "player_name": "string",
#   "score": "integer",
#   "turn_order": "integer"
# }
def create_player(game_id, name, order):
    player = {
        'id': "player_" + hash_string(game_id + "_" + name),
        'game_id': game_id,
        'player_name': name,
        'score': 0,
        'turn_order': order
    }
    table_player.put_item(Item=player)

    response = {
        'player_id': player['id'],
        'player_name': name,
        'score': 0,
        'turn_order': order
    }
    return response  
    
# {
#   "players": ["string"]
# }
def create_game(request_body):
    now = time.time()
    
    game_id = 'game_' + hash_string(str(now) + str(request_body['players']))
    
    players = []
    for index, player_name in enumerate(request_body['players']):
        player = create_player(game_id, player_name, index)
        players.append(player)

    squares = []
    categories = get_categories()
    for c_id, c in enumerate(categories):
        questions = get_questions(c['name'])
        for q_id, q in enumerate(questions):
            square = {
                "position": {
                    "facet": c_id,
                    "position_id": q_id 
                },
                "question": {
                    "question_id": q["id"],                    
                    "question_text": q["question_text"],                    
                    "media_url": q["media_url"],                    
                    "category_name": c["name"],                    
                    "category_color": c["color"],                    
                }
            }
            squares.append(square)
            print(square)
    
    game = {
        "id": game_id,
        "created_at": int(now),
        "status": "ready",
        "players": players,
        "squares": squares
    }

    table_game.put_item(Item=game)
    
    return {
        'statusCode': 200,
        'body': json.dumps(game)
    }

def update_game(data):
    game_id = data['id']

    games = table_game.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('id').eq(game_id)
    )
    
    items = games["Items"]
    converted = replace_decimals(items)
    game = converted[0]
    print(f"game={game}")
    
    if game['status'] == 'ready':
        game['status'] = 'started'
    
    question_id = data['question_id']
    question_response = table_question.get_item(Key={"id": question_id})
    question = question_response["Item"]
    print(f"question={question}")

    actual_answer = question["answer"]
    attempted_answer = data["answer"].lower()
    if actual_answer == attempted_answer:
        player_id = data['player_id']
        player_response = table_player.get_item(Key={"id": player_id})
        print(f"player_response={player_response}")
        player = player_response["Item"]
        
        table_player.update_item(
            Key={'id': player_id},
            AttributeUpdates={
                'score': player["score"] + 1
            },
        )
        
    return {
        'statusCode': 200,
        'body': json.dumps(game)
    }

def lambda_handler(event, context):
    print(f"event={event}")
    print(f"context={context}")

    request_body = json.loads(event['body'])
    operation = request_body['operation']
    if operation == 'create':
        return create_game(request_body['data'])
    elif operation == 'update':
        return update_game(request_body['data'])
    
    raise ValueError(f'Unrecognized operation "{operation}"')
