import pytest
import warnings

# Suppress specific warning types
warnings.filterwarnings("ignore", category=DeprecationWarning)
from unittest.mock import patch
import sys

# Add the path to the directory containing search_pb2.py
sys.path.append('.')  # Adjust the path as per your directory structure

# Import search_pb2 from the correct location
from search_pb2 import GetSearchResponse

# Import the Flask app instance from searchService.py
from searchService import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_render_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode() == "Home"

@patch('searchService.search_client.GetSearch')
def test_search_success(mock_get_search, client):
    # Mock gRPC response
    mock_response = GetSearchResponse()
    song = mock_response.songs.add()
    song.id = 1
    song.title = "Test Song"
    song.artists = "Test Artist"
    
    mock_get_search.return_value = mock_response

    # Test the endpoint with valid parameters
    response = client.get('/regular/search?song=test')
    assert response.status_code == 200
    assert response.json == {
        "songs": [
            {
                "id": 1,
                "title": "Test Song",
                "artists": "Test Artist"
            }
        ]
    }

@patch('searchService.search_client.GetSearch')
def test_search_no_match(mock_get_search, client):
    # Mock gRPC response with no songs
    mock_response = GetSearchResponse()
    mock_get_search.return_value = mock_response

    # Test the endpoint with valid parameters but no matches
    response = client.get('/regular/search?song=nonexistent')
    assert response.status_code == 200
    assert response.data.decode() == "ERROR, NO MATCH"

def test_search_missing_parameters(client):
    # Test the endpoint with missing parameters

    response = client.get('/regular/search')
    assert response.status_code == 200
    assert response.data.decode() == "ERROR ON INPUT"
