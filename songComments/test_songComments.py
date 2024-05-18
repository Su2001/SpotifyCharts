import pytest
from unittest.mock import patch
import sys

# Add the path to the directory containing songComments_pb2.py
sys.path.append('.')  # Adjust the path as per your directory structure

# Import songComments_pb2 from the correct location
from songComments_pb2 import (
    AddCommentResponse,
    UpdateCommentResponse,
    RemoveCommentResponse
)

# Import the Flask app instance from SongCommentsService.py
from SongCommentsService import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == "ok"

def test_non(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == "ok"

# Mock gRPC responses for testing add, update, and remove comment endpoints
@patch('SongCommentsService.songComments_client.Add')
def test_add_comment(mock_add, client):
    mock_response = AddCommentResponse(response=1)  # Modify as per your response structure
    mock_add.return_value = mock_response

    # Test the endpoint with valid parameters
    response = client.post('/premium/song-details/1/comment?user_id=1&comment=test')
    assert response.status_code == 200
    assert response.json == 1  # Assuming your response returns the comment ID

@patch('SongCommentsService.songComments_client.Update')
def test_update_comment(mock_update, client):
    mock_response = UpdateCommentResponse(response=1)  # Modify as per your response structure
    mock_update.return_value = mock_response

    # Test the endpoint with valid parameters
    response = client.put('/premium/song-details/1/comment/1?user_id=1&comment=test')
    assert response.status_code == 200
    assert response.json == 1  # Assuming your response returns the updated comment ID

@patch('SongCommentsService.songComments_client.Remove')
def test_remove_comment(mock_remove, client):
    mock_response = RemoveCommentResponse(response=1)  # Modify as per your response structure
    mock_remove.return_value = mock_response

    # Test the endpoint with valid parameters
    response = client.delete('/premium/song-details/1/comment/1?user_id=1')
    assert response.status_code == 200
    assert response.json == 1  # Assuming your response returns the removed comment ID
