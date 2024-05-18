import pytest
from unittest.mock import patch
import sys

# Add the path to the directory containing playlist_pb2.py
sys.path.append('.')

from playlist_pb2 import GetPlayListResponse, ModifyPlayListRequest
from playlist_pb2_grpc import PlayListServiceStub
from PlayListService import app

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

@patch('PlayListService.playList_client.Get')
def test_get_PlayList_success(mock_get, client):
    mock_response = GetPlayListResponse(response=1)
    # song = mock_response.songs.add()
    # song.id = 1
    # song.title = "Test Song"
    # song.artists = "Test Artist"
    # mock_get.return_value = mock_response

    with client.session_transaction() as sess:
        sess['google_id'] = 'test_google_id'
        sess['name'] = 'Test User'

    response = client.get('/premium/playlist', query_string={'user_id': 1})
    # assert response.status_code == 200

@patch('PlayListService.playList_client.Add')
def test_add_PlayList_success(mock_add, client):
    # Mock gRPC response
    mock_add.return_value = None  # No response needed for this test

    # Test the endpoint
    response = client.post('/premium/playlist/1', json={'user_id': 1})

@patch('PlayListService.playList_client.Add')
def test_add_PlayList_failure(mock_add, client):
    # Mock gRPC response
    mock_add.return_value = None  # No response needed for this test

    # Test the endpoint
    response = client.post('/premium/playlist/1', json={'user_id': 1})
    

@patch('PlayListService.playList_client.Remove')
def test_remove_PlayList_success(mock_remove, client):
    # Mock gRPC response
    mock_remove.return_value = None  # No response needed for this test

    # Test the endpoint
    response = client.delete('/premium/playlist/1', query_string={'user_id': 1})

@patch('PlayListService.playList_client.Remove')
def test_remove_PlayList_failure(mock_remove, client):
    # Mock gRPC response
    mock_remove.return_value = None  # No response needed for this test

    # Test the endpoint
    response = client.delete('/premium/playlist/1', query_string={'user_id': 1})
