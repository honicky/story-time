from fastapi import HTTPException
import pytest
from .api import extract_latest_selections


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
