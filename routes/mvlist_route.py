import datetime
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from config.db import get_database
import random
from typing import List

router = APIRouter()
db = get_database().sample_mflix
db1 = get_database()
# print(list(db.movies.find().limit(1)))
# print("users:", db1.scores.scores.find({}))
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

 
@router.post("/create-user")
async def create_user(username: str):
    random_movie = await get_random_movie()
    user_data = {
        "name": username,
        "assigned_movie": random_movie,
        "start_time": datetime.datetime.now()
    }

    result = db1.scores.scores.insert_one(user_data)
    return {
        "user_id": str(result.inserted_id),
        "name": username,
        "assigned_movie": random_movie,
        "start_time": user_data["start_time"]
    }

@router.put("/end-game/{user_id}")
async def end_game(user_id: str):
    end_time = datetime.datetime.now()
    user = db1.scores.scores.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    time_taken = (end_time - user["start_time"]).total_seconds()
    
    db1.scores.scores.update_one(
        {"_id": ObjectId(user_id)},
        {
            "$set": {
                "end_time": end_time,
                "time_taken": time_taken
            }
        }
    )
    
    return {
        "name": user["name"],
        "time_taken": time_taken
    }

# @router.post("/predict-movie")
# async def predict_movie(emojis: str):
#         # This endpoint just receives emojis and returns prediction
#         predicted_movie = "Model_Prediction"  # Replace with actual model call
        
#         return JSONResponse(
#             content={
#                 "status": "success",
#                 "predicted_movie": predicted_movie,
#                 "confidence": 0.85  # Example confidence score
#             }
#         )

# router.post("/verify-guess/{user_id}")
# async def verify_guess(user_id: str, predicted_movie: str):
#     user = db1.scores.scores.find_one({"_id": ObjectId(user_id)})
#     if not user:
#         return JSONResponse(
#             status_code=404,
#             content={"status": "error", "message": "User not found"}
#         )
  
#     is_correct = predicted_movie == user["assigned_movie"]["title"]
    
#     return JSONResponse(
#         content={
#             "status": "success",
#             "correct": is_correct,
#             "actual_movie": user["assigned_movie"]["title"] if is_correct else None
#         }
#     )

    
# router.get("/leaderboard")
# async def get_leaderboard(limit: int = 10):
#     leaderboard = list(db1.scores.scores.find(
#         {"time_taken": {"$exists": True}},
#         # {"name": 1, "time_taken": 1, "emoji_attempts": 1, "_id": 0}
#         {"name": 1, "time_taken": 1, "_id": 0}
#     ).sort("time_taken", 1).limit(limit))
    
#     return JSONResponse(
#         content={
#             "status": "success",
#             "data": leaderboard
#         }
#     )

for user in db1.scores.scores.find({}).sort("time_taken"):
    print(user, "\n")