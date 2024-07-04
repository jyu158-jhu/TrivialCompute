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

def get_categories(category_count):
    scan_kwargs = {
        "Limit": category_count
    }
    categories = table_category.scan(**scan_kwargs)
    print(f"categories={categories}")
    return categories['Items']


def get_questions(category_name, count):
    questions = table_question.query(
        IndexName="category_name-index",
        KeyConditionExpression=boto3.dynamodb.conditions.Key('category_name').eq(category_name),
        Limit=count
    )
    
    # print(f"category={category_name}, questions={questions}")
    return questions['Items']
    
    
def hash_string(string):
    h = hashlib.new('md5')
    h.update(string.encode())
    return h.hexdigest()

# {
#   "score": "integer",
#   "turn_order": "integer"
# }
def create_player(order):
    player = {
        'score': 0,
        'turn_order': order
    }

    return player  
    
# {
#   "players": ["string"],
#   "category_count": int,
#   "questions_per_category": int,
# }
def create_game(request_body):
    now = time.time()
    
    game_id = 'game_' + hash_string(str(now) + str(request_body['players']))
    
    players = {}
    for index, player_name in enumerate(request_body['players']):
        player = create_player(index)
        players[player_name] = player

    category_count = request_body["category_count"]
    questions_per_category = request_body["questions_per_category"]

    squares = {}
    categories = get_categories(category_count)
    for c_id, c in enumerate(categories):
        questions = get_questions(c['name'], questions_per_category)
        for q_id, q in enumerate(questions):
            square_position = f"{c_id},{q_id}"
            question= {
                "question_id": q["id"],
                "question_text": q["question_text"],
                "media_url": q["media_url"],
                "category_name": c["name"],
                "category_color": c["color"],
                "answered_by": "",
                "answered_at": 0,
                "answer": "",
                "answer_score": 0
            }
            squares[square_position] = question

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

def update_square(game, square_position, player_name, answer):
    question_id = game["squares"][square_position]["question_id"]
    question_response = table_question.get_item(Key={"id": question_id})
    question = question_response["Item"]
    print(f"question={question}")

    actual_answer = question["answer"]

    now = int(time.time())
    game['squares'][square_position]["answer"] = answer
    game['squares'][square_position]["answered_at"] = now
    game['squares'][square_position]["answered_by"] = player_name

    result = False
    if actual_answer == answer.lower():
        game["player"][player_name]["score"] += 1
        game['squares'][square_position]["answer_score"] = 1
        result = True

    return result, game


def check_game_end(game):
    for square in game["squares"].values():
        if square["answered_at"] == 0:
            return False
    return True

# {
#     "operation": "update",
#     "data": {
#         "id": "game_bbd72496707d12ccedf2fd334838e02f",
#         "position": "0,0",
#         "player_name": "player_a",
#         "answer": "Carbon Dioxide"
#     }
# }
def update_game(data):
    game_id = data['id']

    games = table_game.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('id').eq(game_id)
    )
    
    if "Items" not in games:
        return {
            'statusCode': 400,
            'body': f"invalid game id: {game_id}"
        }
        
    items = games["Items"]
    converted = replace_decimals(items)
    game = converted[0]
    print(f"game={game}")
    
    if game['status'] == 'ready':
        game['status'] = 'started'
    elif game['status'] == 'finished':
        return {
            'statusCode': 400,
            'body': f"game has finished"
        }

    position = data["position"]
    answer = data["answer"].lower()
    player_name = data["player_name"]

    result, updated_game = update_square(game, position, player_name, answer)
    print(f"updated_game={updated_game}")
    
    if check_game_end(game):
        game['status'] = 'finished'
    
    table_game.put_item(Item=updated_game)

    response = {
        "result": result,
        "updated_game": updated_game
    }
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def lambda_handler(event, context):
    print(f"event={event}")
    print(f"context={context}")

    request_body = json.loads(event['body'])
    print(f"request_body={request_body}")

    if 'operation' not in request_body:
        return {
            'statusCode': 400,
            'body': f'request body misses operation'
        }

    if 'data' not in request_body:
        return {
            'statusCode': 400,
            'body': f'request body misses data'
        }

    operation = request_body['operation']
    if operation == 'create':
        return create_game(request_body['data'])
    elif operation == 'update':
        return update_game(request_body['data'])
    
    return {
        'statusCode': 400,
        'body': f'Unrecognized operation "{operation}"'
    }
