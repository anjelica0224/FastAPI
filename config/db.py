from pymongo import MongoClient
import os
from dotenv import load_dotenv

def get_database():
    load_dotenv()
    url = os.getenv('Database_URI')
    # print("url is :" , url)
    connection = MongoClient(url)
    return connection.scores
