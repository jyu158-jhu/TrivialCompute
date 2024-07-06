# Trivial Compute API

Here's a basic design for the RESTful API for the Trivial Compute game, covering endpoints for games, players, questions, categories, and game board squares.

## Example API Workflow
### Setup before starting games

Create a new category (POST /categories)
Create a list of question (POST /questions)

### Game flow

Create a new game board (POST /games)
Post an answer to a square on the board (POST /games)

### Postgame
	
Get game details, including players and asked questions (GET /games/{game_id})

## Endpoints
### Categories
#### Create a new category
```
POST /categories
```
    
Request Body:
```
{
  "name": "string",
  "color": "string"
}
```

Response:
```
{
  "id": "string",
  "name": "string",
  "color": "string"
}
```

https://jthtbqx5pk.execute-api.us-west-2.amazonaws.com/prod/categories 


#### Get all categories

GET /categories


Response:
```
[
  {
    "category_id": "string",
    "category_name": "string",
    "color": "string"
  }
]
```


### Questions

#### Create a new question
```
POST /questions
```

Request Body:
```
[
  {
    "category_name": "string",
    "question_text": "string",
    "answer": "string",
    "media_url": "string"
  }
]
```

Response:

```
[
  {
    "id": "string",
    "category_name": "string",
    "question_text": "string",
    "answer": "string",
    "media_url": "string"
  }
]
```

https://8dibhaiy86.execute-api.us-west-2.amazonaws.com/prod/questions 


#### Get question details
```
GET /questions?category=<category_name>
```

Response:
```
{
  "id": "string",
  "category_name": "string",
  "question_text": "string",
  "answer": "string",
  "media_url": "string",
}
```

https://8dibhaiy86.execute-api.us-west-2.amazonaws.com/prod/questions?category=literature 



### Games
#### Create a new game
```
POST /games
```
 
Request Body:
```
{
  "operation": "create",
  "data": {
    "players": ["string"],
    "category_count": int,
    "questions_per_category": int
  }
}
```

Response:
```
{
  "id": "string",
  "created_at": integer,
  "status": "string",
  "players": {
    "player_name": {
      "score": integer,
      "turn_order": integer
    }
  },
  "squares": {
    "square_position": {
      "question_id": "string",
      "question_text": "string",
      "media_url": "string",
      "category_name": "string",
      "category_color": "string",
      "answered_by": "string",
      "answered_at": integer,
      "answer": "string",
      "answer_score": integer
    }
  }
}
```

https://8dwqjz2mlb.execute-api.us-west-2.amazonaws.com/prod/games


#### Get game details
```
GET /games?id={game_id}
```
```
Response:

{
  "id": "string",
  "created_at": integer,
  "status": "string",
  "players": {
    "player_name": {
      "score": integer,
      "turn_order": integer
    }
  },
  "squares": {
    "square_position": {
      "question_id": "string",
      "question_text": "string",
      "media_url": "string",
      "category_name": "string",
      "category_color": "string",
      "answered_by": "string",
      "answered_at": integer,
      "answer": "string",
      "answer_score": integer
    }
  }
}
```



### Answer a square on a game board square
```
POST /games
```

Request Body:
```
{
  "operation": "update",
  "data": {
    "id": "string",
    "position": "string",
    "player_name": "string",
    "answer": "string"
  }
}
```

Response:
```
{
  "result": boolean,
  "updated_game": {
    "id": "string",
    "created_at": "timestamp",
    "status": "string",
    "players": {
      "player_name": {
        "score": "integer",
        "turn_order": "integer"
      }
    },
    "squares": {
      "square_id": {
        "question_id": "string",
        "answered_at": "timestamp",
        "score": "integer",
      }
    }
  }
}
```




Github Repo
