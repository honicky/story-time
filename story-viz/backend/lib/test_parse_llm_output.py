import pytest
from parse_llm_output import find_first_json_array_of_strings, count_chars_outside_first_json_array

def test_find_first_json_array_of_strings():
    assert find_first_json_array_of_strings('["One", "Two", "Three"]') == '["One", "Two", "Three"]'
    assert find_first_json_array_of_strings('No JSON here!') is None
    assert find_first_json_array_of_strings('Prefix text ["First", "Second"] suffix text') == '["First", "Second"]'
    assert find_first_json_array_of_strings('Prefix text ["First", "Second"] suffix text ["Third", "Fourth"] suffix2') == '["First", "Second"]'

def test_count_chars_outside_first_json_array():
    assert count_chars_outside_first_json_array('["One", "Two", "Three"]') == 0
    assert count_chars_outside_first_json_array('Prefix text ["First", "Second"] suffix text') == 24  # Length of 'Prefix text ' and ' suffix text'
    assert count_chars_outside_first_json_array('Prefix text ["First", "Second"] suffix text ["Third", "Fourth"] suffix2') == 52  # Length of 'Prefix text ' and ' suffix text ["Third", "Fourth"] suffix2'
    assert count_chars_outside_first_json_array('No JSON here!') == 13  # Entire input is considered outside since there's no JSON array
    assert count_chars_outside_first_json_array('["One", "Two", ["Three", "Four"]]') == 16 
