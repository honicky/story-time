
from datetime import datetime
from beam import App, Image, Runtime
from bson.objectid import ObjectId
from bson.json_util import dumps as bson_dumps
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from typing import List
import os
from pymongo.collection import ReturnDocument
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


app = App(
    name="story-viz",
    runtime=Runtime(
        cpu=1,
        memory="128Mi",
        gpu="",
        image=Image(
            python_packages=["pymongo[srv]"],
        )

    ),
)

mongodb_password = os.environ['MONGODB_STORY_TIME_EDITOR_PASSWORD']
mongo_uri = f"mongodb+srv://story_time_editor:{mongodb_password}@freecluster.wk9cvp6.mongodb.net/?retryWrites=true&w=majority"

api = FastAPI()
mongo_client = MongoClient(mongo_uri, server_api=ServerApi('1'))


@app.asgi(authorized=False)
def handler():

    def mongodb_json_response(data):
        return Response(content=bson_dumps(data), media_type="application/json")
    
    @api.get("/ping")
    def ping(): 

        mongo_client.admin.command('ping')
        return "Pinged your deployment. You successfully connected to MongoDB!"

    @api.get("/story/{story_id}")
    def get_story(story_id: str):
        story = mongo_client.story_time.stories.find_one({"_id": ObjectId(story_id)})
        return mongodb_json_response(story)

    @api.get("/story/")
    def get_stories():
        stories = mongo_client.story_time.stories.find({}, {"_id": 1})
        return [str(oid["_id"]) for oid in stories]

    class Selection(BaseModel):
        page_selections: List[int]

    @api.post("/story/{story_id}/selections")
    def set_story_selections(story_id: str, selection: Selection):
        # Retrieve the story to get the number of images per page
        story = mongo_client.story_time.stories.find_one({"_id": ObjectId(story_id)})
        if not story:
            raise HTTPException(status_code=404, detail="Story not found")
        if "pages" not in story:
            raise HTTPException(status_code=404, detail="Story does not contain pages")

        # Validate the selections
        for page_index, image_index in enumerate(selection.page_selections):
            if page_index < 0 or page_index >= len(story["pages"]):
                raise HTTPException(status_code=400, detail=f"Invalid page index: {page_index}")
            if image_index < 0 or image_index >= len(story["pages"][page_index]["image_urls"]):
                raise HTTPException(status_code=400, detail=f"Invalid image index for page {page_index}")

        if len(selection.page_selections) != len(story["pages"]):
            raise HTTPException(status_code=400, detail=f"Invalid number of selections: {len(selection.page_selections)}")

        # Append the new selection to the array in the "selections" collection
        updated_selection = mongo_client.story_time.selections.find_one_and_update(
            {"story_id": ObjectId(story_id)},
            {
                "$push": {
                    "selections": {
                        "timestamp": datetime.now(),
                        "selections": selection.page_selections
                    }
                }
            },
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        return mongodb_json_response(updated_selection)

    @api.get("/story/{story_id}/selections")
    def get_story_selections(story_id: str):
        selection = mongo_client.story_time.selections.find_one({"story_id": ObjectId(story_id)})
        if not selection:
            raise HTTPException(status_code=404, detail="Selections for story not found")

        return mongodb_json_response(selection['selections'])

    @api.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        exception_messsage = f"Unhandled exception: {exc} - Path: {request.url.path}" 
        print(exception_messsage)
        return JSONResponse(
            status_code=500,
            content={"message": exception_messsage}
        )

    return api


