from bson import ObjectId
from fastapi import HTTPException
import pytest
from .api import extract_latest_selections
from .api import get_image_prompt
from .api import update_images
from .api import validate_selection, Selection
from .api import validate_story
import mongomock
from unittest.mock import patch


def test_extract_latest_selections_empty():
    selections = {"selections": []}
    story = {"pages": [1, 2, 3]}

    with pytest.raises(Exception):
        extract_latest_selections(selections, story)


def test_extract_latest_selections_missing_key():
    selections = {"selections": [{}]}
    story = {"pages": [1, 2, 3]}

    with pytest.raises(HTTPException):
        extract_latest_selections(selections, story)


def test_validate_selection_valid():
    selection = Selection(page_selections=[0, 1])
    story = {"pages": [{"image_urls": [1, 2]}, {"image_urls": [3, 4]}]}

    validate_selection(selection, story)


def test_validate_selection_invalid_page():
    selection = Selection(page_selections=[0, 3])
    story = {"pages": [{"image_urls": [1, 2]}, {"image_urls": [3, 4]}]}

    with pytest.raises(HTTPException):
        validate_selection(selection, story)


def test_validate_selection_invalid_image():
    selection = Selection(page_selections=[0, 2])
    story = {"pages": [{"image_urls": [1, 2]}, {"image_urls": [3, 4]}]}

    with pytest.raises(HTTPException):
        validate_selection(selection, story)


def test_validate_selection_mismatch_pages():
    selection = Selection(page_selections=[0])
    story = {"pages": [{"image_urls": [1, 2]}, {"image_urls": [3, 4]}]}

    with pytest.raises(HTTPException):
        validate_selection(selection, story)


def test_validate_story_valid():
    story = {"pages": [{"image_urls": [1, 2]}]}
    validate_story(story)


def test_validate_story_missing():
    with pytest.raises(HTTPException):
        validate_story(None)


def test_validate_story_no_pages():
    story = {}
    with pytest.raises(HTTPException):
        validate_story(story)


story = {
    "pages": [
        {"image_prompt": ["First page prompt 1", "First page prompt 2"]},
        {"image_prompt": ["Second page prompt 1", "Second page prompt 2"]},
        {"image_prompt": ["Third page prompt 1", "Third page prompt 2"]},
    ]
}


def test_valid_input():
    prompt = get_image_prompt(story, 1)
    assert prompt == "Second page prompt 2", "The function should return the last image prompt of the second page"


def test_negative_page_index():
    with pytest.raises(HTTPException) as excinfo:
        get_image_prompt(story, -1)
    assert "Invalid page index" in str(
        excinfo.value.detail
    ), "The function should raise an HTTPException for negative page index"


def test_page_index_out_of_range():
    with pytest.raises(HTTPException) as excinfo:
        get_image_prompt(story, len(story["pages"]))
    assert "Invalid page index" in str(
        excinfo.value.detail
    ), "The function should raise an HTTPException for out-of-range page index"


def test_first_page_prompt():
    prompt = get_image_prompt(story, 0)
    assert prompt == "First page prompt 2", "The function should return the last image prompt of the first page"


def test_last_page_prompt():
    prompt = get_image_prompt(story, len(story["pages"]) - 1)
    assert prompt == "Third page prompt 2", "The function should return the last image prompt of the last page"


@pytest.fixture
def mock_mongo_client():
    """Fixture to create a mongomock client."""
    client = mongomock.MongoClient()
    yield client


def test_update_images_success(mock_mongo_client):
    # Use the mongomock client for your database operations
    mock_db = mock_mongo_client.story_time
    stories_collection = mock_db.stories

    # Insert a dummy document to simulate existing data
    story_id = stories_collection.insert_one({"_id": ObjectId(), "pages": [{"image_urls": []}]}).inserted_id
    page_index = 0
    image_urls = ["http://example.com/image1.jpg", "http://example.com/image2.jpg"]

    # Patch the mongo_client used in your function to use the mock_mongo_client
    with patch('backend.api.mongo_client', mock_mongo_client):
        response = update_images(str(story_id), page_index, image_urls)
    assert response.status_code == 200

    # Verify the update in the mock database
    updated_story = stories_collection.find_one({"_id": story_id})
    assert image_urls == updated_story["pages"][page_index]["image_urls"]
