from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pymongo.mongo_client import MongoClient
from pymongo.errors import OperationFailure
from schemas import Resource
from typing import List

import os
from dotenv import load_dotenv
load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")


client = MongoClient('mongodb://localhost:27017/')
database = client[DB_NAME]


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_credentials = True,
    allow_headers = ["*"]
)  

try:
    database['Resources'].create_index([('title', 'text'), ('value', 'text')])
except OperationFailure as e:
    print(e)


@app.get('/search/{search_text}', response_model=List[Resource])
def search_resources(search_text: str):
    results = database['Resources'].find({"$text": {"$search": search_text}}).limit(10)
    return results

@app.get('/tables', response_model=List[Resource])
def get_tables():
    results = database['Resources'].find({"title": "table"}).limit(20)
    return results

