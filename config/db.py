import csv
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
def get_database():
    load_dotenv()
    # url = os.getenv('Database_URI')
    # # print("url is :" , url)
    # connection = MongoClient(url)
    # return connection.scores
    url = os.getenv("uri")
    client = MongoClient(url,
        server_api=ServerApi('1')
    )
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
        return None
    
def movie_list():
    list = os.getenv("file_path")
    with open(list, 'r', encoding='utf-8') as file:
            csvReader = csv.DictReader(file)
            titles = []
            for row in csvReader:
                titles.append(row['Title'])  
    return titles


