
import datetime
from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from pymongo import ReturnDocument
from config.db import get_database, movie_list
import random
from models.user import User, UpdateUser, User_List, UserScore

router = APIRouter()
db1 = get_database()
collection = db1.scores.scores

@router.get("/movies")
async def get_movies():
    titles = movie_list()
    return JSONResponse(
            content={
                "status": "success",
                "movies": titles,
                "count": len(titles)
            }
    )

# @router.get("/random-movie")
def get_random_movie():
    random_movie = random.choice(movie_list())
    return random_movie


@router.post("/user/", response_description="Add new user")
async def create_user(username: str):
    user = User(
        username = username,
        assigned_movie = None,
        start_time = None,
        emoji_string = "",
        emoji_count = 0
    )

    result = collection.insert_one(user.dict(exclude_none = True))
    created_user = collection.find_one({"_id": result.inserted_id})
    return User(**created_user)
            

@router.put("/user/{user_id}")
async def assign_movie(user_id: str):
    random_movie = get_random_movie()
    start_time = datetime.datetime.now()

    update_data = UpdateUser(
        assigned_movie = random_movie,
        start_time=start_time
    )  
    updated_user = collection.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": update_data.dict(exclude_none=True)},
        return_document=True 
    )
    return User(**updated_user), random_movie

# ml-model comes here
ML_Model_prediction = "Interstellar" 

@router.post("check-guess/{user_id}")
async def check_guess(user_id: str, emoji_string: str):
    user = collection.find_one({"_id": ObjectId(user_id)})
    update_data = UpdateUser(
            emoji_string=emoji_string,
            emoji_count=len(emoji_string)
    )
    is_correct = ML_Model_prediction == user["assigned_movie"]
    if is_correct:
        end_time = datetime.datetime.now()
        time_taken = (end_time - user["start_time"]).total_seconds()
        update_data.end_time = end_time
        update_data.time_taken = time_taken
        update_data.success = True
        collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": update_data.dict(exclude_none=True)}
        )
        return ML_Model_prediction
    
    else :
        update_data.success = False
        updated_user = collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": update_data.dict(exclude_none=True)},
            return_document=True
        )
        return User(**updated_user), "OOPS"


@router.get("/user/", response_model=User_List, response_model_by_alias=False, response_description="list of users")
async def get_users():
    users = collection.find(
            {"time_taken": {"$exists": True}},
            {"username": 1, "time_taken": 1, "emoji_count": 1, "_id": 1}
        ).to_list(1000)
    return User_List(total_players= users)

