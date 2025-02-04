from fastapi import APIRouter, HTTPException
from config.db import get_database
import random
from typing import List

router = APIRouter()
db = get_database()

# print(list(db.movies.find().limit(1)))

# movie_count = db.movies.count_documents({})
# print(f"Total movies: {movie_count}")

# print("random --- ", random_movie)
    
@router.get("/movies", response_model=List[dict])
async def get_movies(limit: int = 10):
    movies = list(db.movies.find({}, 
                                {"title": 1, "genres": 1, "year": 1, "_id": 0})
                    .limit(limit))
    return movies

@router.get("/random-movie")
async def get_random_movie():

    total_movies = db.movies.count_documents({})
    # Generate random skip value
    # random_skip = random.randint(0, total_movies - 1)
    # # Get random movie
    # random_movie = db.movies.find_one({}, 
    #                                 {"title": 1, "genres": 1, "year": 1, "_id": 0}, 
    #                                 skip=random_skip)
    print("hello")
    random_movie = list(db.movies.aggregate([
            { "$sample": { "size": 1 } },
            { "$project": {
                "_id": 0,
                "title": 1,
                "year": 1,
                "genres": 1
            }}
        ]))
    return random_movie
