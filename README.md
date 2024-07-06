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
<img width="770" alt="image" src="https://github.com/jyu158-jhu/TrivialCompute/assets/173595847/16051716-208b-4a42-b459-f88633363a91">
<img width="766" alt="image" src="https://github.com/jyu158-jhu/TrivialCompute/assets/173595847/d003a2d3-3c8e-4564-b6b4-9582156049ec">


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
<img width="771" alt="image" src="https://github.com/jyu158-jhu/TrivialCompute/assets/173595847/72464e24-78fe-4078-8bb2-b46a62c13eb7">


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
<img width="760" alt="image" src="https://github.com/jyu158-jhu/TrivialCompute/assets/173595847/9825a06d-3f46-4dd9-a356-86959802b75b">
<img width="770" alt="image" src="https://github.com/jyu158-jhu/TrivialCompute/assets/173595847/5b32708d-04a3-4633-ab25-93844a9f8e1a">


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

<img width="763" alt="image" src="https://github.com/jyu158-jhu/TrivialCompute/assets/173595847/30bbf96c-c10e-476b-9fef-2a71673f7a62">
<img width="773" alt="image" src="https://github.com/jyu158-jhu/TrivialCompute/assets/173595847/2248475b-f320-4f01-8582-fd1e85a31d45">


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
<img width="760" alt="image" src="https://github.com/jyu158-jhu/TrivialCompute/assets/173595847/5a40fd3a-8fb8-4234-b852-b39e0be209af">
<img width="772" alt="image" src="https://github.com/jyu158-jhu/TrivialCompute/assets/173595847/13490732-53b2-43de-8b72-4d22f8fabe4e">


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

<img width="756" alt="image" src="https://github.com/jyu158-jhu/TrivialCompute/assets/173595847/089d32b7-6c1d-4107-843a-c63f59ec6686">


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

<img width="767" alt="image" src="https://github.com/jyu158-jhu/TrivialCompute/assets/173595847/ccecfaa8-d8ce-4b83-b00e-2bc9ca7b75ac">
<img width="769" alt="image" src="https://github.com/jyu158-jhu/TrivialCompute/assets/173595847/f306e8c8-4dde-4a7d-9f7f-d4bce62f8b5e">

