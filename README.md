# Video Recommendation Engine

This project implements a hybrid video recommendation engine using FastAPI. It supports two modes of recommendation:

Graph-Based Recommendations: Users are connected via a graph where edges represent similarity in interactions (likes, views, ratings). The system recommends videos liked or interacted with by top similar users.

Semantic Ranking via Deep Learning: When a textual query or category is provided, the system uses a pre-trained sentence transformer model (BAAI/bge-base-en-v1.5) to embed both the query and rich video metadata (title, description, themes, keywords, etc.). Cosine similarity between embeddings ranks videos based on semantic relevance.

## Clone the project

```
https://github.com/ayushpareek2003/video-recommendation-assignment.git
```

## Run local

### Install dependencies

```
cd video-recommendation-assignment
pip install -r requirements.txt
```

### Run server

```
uvicorn app.main:app --reload
```

### Example Output From endpoint

```
    {
        "id": 63,
        "title": "This app is literally steroids for your brain",
        "upvote_count": 66,
        "video_link": "https://video-cdn.socialverseapp.com/jack_9fe743fe-5749-498b-a3f0-f6d7bbb97fe1.mp4",
        "username": "jack"
    },
    {
        "id": 82,
        "title": "Decide to be extraodinary and do",
        "upvote_count": 33,
        "video_link": "https://video-cdn.socialverseapp.com/kinha_db5268a0-e503-4ab3-8ac4-fb0990d7d478.mp4",
        "username": "kinha"
    },
```

## API documentation (provided by Swagger UI)
```
http://127.0.0.1:8000/docs
```

## Tech Stack Used 
Machine Learning & NLP
SentenceTransformer – semantic embeddings for text (model: BAAI/bge-base-en-v1.5)

PyTorch – backend for computing cosine similarity between embeddings

numpy – for sorting and numerical operations

re (regex) – for parsing structured descriptions

🛠️ Backend / API
FastAPI – for building the /feed API endpoint

Pydantic / Query – for query parameter validation and typing

🗃️ Database
MongoDB – stores user and post data

pymongo – MongoDB Python client
