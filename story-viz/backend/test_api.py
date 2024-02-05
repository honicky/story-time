from fastapi import HTTPException
import pytest
from .api import extract_latest_selections
from .api import validate_selection, Selection
from .api import validate_story


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
