
from datetime import datetime, timedelta
# from beam import App, Image, Runtime
import boto3
from botocore.exceptions import ClientError
from bson.objectid import ObjectId
from bson.json_util import dumps as bson_dumps
from dotenv import load_dotenv
import json
import jwt
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import List, Optional
import os
from pymongo.collection import ReturnDocument
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from lib import object_store_client

load_dotenv()  # take environment variables from .env if they exist

mongodb_password = os.environ['MONGODB_STORY_TIME_EDITOR_PASSWORD']
mongo_uri = f"mongodb+srv://story_time_editor:{mongodb_password}@freecluster.wk9cvp6.mongodb.net/?retryWrites=true&w=majority"

jwt_secret_key = os.environ["JWT_SECRET_KEY"]
JWT_ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

hard_coded_users_db = {
    "rj": {
        "username": "rj",
        "hashed_password": "$2b$12$C1jTodI/Dw24k76WIxac/.oTi2.quoccA/AA9D3LixQRi4PgyiQ/m",
    }
}

api = FastAPI()
mongo_client = MongoClient(mongo_uri, server_api=ServerApi('1'))

# JWT authentication 

pwd_context = CryptContext(schemes=["bcrypt"])
salt = "C1jTodI/Dw24k76WIxac/."

# Pydantic models for user and token
class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def verify_password(plain_password, hashed_password):
    print(f"{plain_password}, {hashed_password}")
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    print(f"{username}, {db}")
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(user_db, username: str, password: str):
    user = get_user(user_db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=90)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_secret_key, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, jwt_secret_key, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user(hard_coded_users_db, username=username)
        if user is None:
            raise credentials_exception
        return user
    except jwt.PyJWTError:
        raise credentials_exception

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, jwt_secret_key, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user(hard_coded_users_db, username=username)
        if user is None:
            raise credentials_exception
        return user
    except jwt.PyJWTError:
        raise credentials_exception

    async def get_current_user(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, jwt_secret_key, algorithms=[JWT_ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            user = get_user(hard_coded_users_db, username=username)
            if user is None:
                raise credentials_exception
            return user
        except jwt.PyJWTError:
            raise credentials_exception



def mongodb_json_response(data):
    return Response(content=bson_dumps(data), media_type="application/json")

@api.get("/api/ping")
def ping(current_user: User = Depends(get_current_user)): 
    mongo_client.admin.command('ping')
    return "Pinged your deployment. You successfully connected to MongoDB!"

@api.get("/api/story/{story_id}")
def get_story(story_id: str, current_user: User = Depends(get_current_user)):
    story = mongo_client.story_time.stories.find_one({"_id": ObjectId(story_id)})
    return mongodb_json_response(story)

@api.get("/api/story/")
def get_stories(current_user: User = Depends(get_current_user)):
    stories = mongo_client.story_time.stories.find()
    return mongodb_json_response(list(stories))

class Selection(BaseModel):
    page_selections: List[int]

@api.post("/api/story/{story_id}/selections")
def set_story_selections(story_id: str, selection: Selection, current_user: User = Depends(get_current_user)):
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

@api.get("/api/story/{story_id}/selections")
def get_story_selections(story_id: str, current_user: User = Depends(get_current_user)):
    selection = mongo_client.story_time.selections.find_one({"story_id": ObjectId(story_id)})
    if not selection:
        raise HTTPException(status_code=404, detail="Selections for story not found")

    return mongodb_json_response(selection['selections'])

@api.post("/api/story/{story_id}/publish")
def publish_story(story_id: str, current_user: User = Depends(get_current_user)):
    '''
    publish a story by taking the latest image selection for the story and removing all of the
    other selections, and then writing the story to the "botos-generated-images" S3 bucket under
    the provided username
    '''   
    
    # Retrieve the story to get the number of images per page
    story = mongo_client.story_time.stories.find_one({"_id": ObjectId(story_id)})
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    if "pages" not in story:
        raise HTTPException(status_code=404, detail="Story does not contain pages")
    
    # Retrieve the latest selection for the story
    selections = mongo_client.story_time.selections.find_one({"story_id": ObjectId(story_id)})
    if not selections:
        raise HTTPException(status_code=404, detail="Selections for story not found")
    if "selections" not in selections:
        raise HTTPException(status_code=404, detail="Selections for story does not contain selections")

    latest_selection = selections["selections"][-1]["selections"]
    if len(latest_selection) != len(story["pages"]):
        raise HTTPException(status_code=400, detail=f"Invalid number of selections: {len(latest_selection)}")

    # Create a new story with the latest selection
    published_story = {
        "pages": []
    }
    print(story["pages"])
    for page_index, image_index in enumerate(latest_selection):
        print(f"page_index: {page_index}, image_index: {image_index}")
        page = story["pages"][page_index]
        published_story["pages"].append({
            "image_url": page["image_urls"][image_index],
            "text": page["paragraph"]
        })

    # Generate the story object key based on the timestamp and username
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    story_object_key = f"{current_user.username}/stories/{timestamp}_story.json"
    # this has to be instatiated inside of the function because of the wierd way that
    # beam handles imports and packages dependencies in the current directory

    s3_client = object_store_client.Boto3Client()

    # Create the S3 client
    bucket_name = "botos-generated-images"

    latest_story_key = f"{current_user.username}/latest_story.json"
    try:
        # Read in the existing 'latest_story.json' file
        json_str = s3_client.get_object(bucket_name, latest_story_key).decode('utf-8')
        latest_stories = json.loads(json_str)
    except ClientError as e:
        # Handle the case where the file does not exist
        if e.response['Error']['Code'] == "NoSuchKey":
            latest_stories = []
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Exception while reading latest_story.json: {e}"
            ) from e

    s3_client.upload_object(json.dumps(published_story), bucket_name, story_object_key)

    latest_stories.insert(0, story_object_key)
    s3_client.upload_object(json.dumps(latest_stories), bucket_name, latest_story_key)

    return {"message": "Story published successfully", "story_key": story_object_key, "latest_story_key": latest_story_key}


@api.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    exception_messsage = f"Unhandled exception: {exc} - Path: {request.url.path}" 
    print(exception_messsage)
    return JSONResponse(
        status_code=500,
        content={"message": exception_messsage}
    )

@api.post("/api/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(hard_coded_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=90)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@api.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user