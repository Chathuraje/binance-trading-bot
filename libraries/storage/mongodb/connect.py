from libraries.config import MONGO_DB_URL, MONGO_DB_USERNAME, MONGO_DB_PASSWORD
from pymongo.mongo_client import MongoClient


def connect_mongodb():
    uri = f"mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@{MONGO_DB_URL}/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        
        return client
    except Exception as e:
        print(e)





