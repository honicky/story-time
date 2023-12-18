from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo.errors
import os

class StoryMongoDB:
    def __init__(self):
        self.username = "story_time_editor"
        self.password = os.environ["MONGODB_STORY_TIME_EDITOR_PASSWORD"]
        self.uri = f"mongodb+srv://{self.username}:{self.password}@freecluster.wk9cvp6.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.db = self.client["story_time"]

    def insert_story(self, story_document):
        # try:

        # Insert the story document into the MongoDB collection
        collection = self.db["stories"]
        result = collection.insert_one(story_document)
        return result.inserted_id

        # except pymongo.errors.WriteError as e:
        #     print(f"Error inserting story: {str(e)}")
        #     return None

    def close_connection(self):
        # Close the MongoDB connection
        self.client.close()