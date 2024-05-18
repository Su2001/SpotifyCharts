import pytest
import warnings

# Suppress specific warning types
warnings.filterwarnings("ignore", category=DeprecationWarning)
from unittest.mock import patch
import sys
import grpc

# Add the path to the directory containing songDetails_pb2.py and songDetails_pb2_grpc.py
sys.path.append('.')

from songDetails_pb2 import GetSongDetailsResponse, SongDetail, Comment
from songDetailsService import app, songDetails_client

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_render_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode() == "Song Details"

@patch.object(songDetails_client, 'GetSongDetails')
def test_song_details_success(mock_get_song_details, client):
    # Mock gRPC response
    comment = Comment(comment_id=1, user_id=1, song_id=1, comment="Test comment")
    song = SongDetail(
        song_id=1,
        title="Test Song",
        artists="Test Artist",
        url="http://example.com",
        numtimesincharts=5,
        numcountrydif=3,
        comments=[comment]
    )
    mock_response = GetSongDetailsResponse(song=song)
    mock_get_song_details.return_value = mock_response

    # Test the endpoint
    response = client.get('/regular/song-details/1')
    assert response.status_code == 200
    assert response.json == {
        "song_id": 1,
        "title": "Test Song",
        "artists": "Test Artist",
        "url": "http://example.com",
        "numtimesincharts": 5,
        "numcountrydif": 3,
        "comments": [
            {
                "comment_id": 1,
                "user_id": 1,
                "song_id": 1,
                "comment": "Test comment"
            }
        ]
    }

@patch.object(songDetails_client, 'GetSongDetails')
def test_song_details_not_found(mock_get_song_details, client):
    # Mock gRPC response for song not found
    mock_response = GetSongDetailsResponse(song=SongDetail())
    mock_get_song_details.return_value = mock_response

    # Test the endpoint
    response = client.get('/regular/song-details/999')
    assert response.status_code == 200
    assert response.json == {
        "song_id": 0,
        "title": "",
        "artists": "",
        "url": "",
        "numtimesincharts": 0,
        "numcountrydif": 0,
        "comments": []
    }

@patch.object(songDetails_client, 'GetSongDetails')
def test_song_details_internal_error(mock_get_song_details, client):
    # Mock gRPC response to raise an exception
    mock_get_song_details.side_effect = grpc.RpcError("Internal error")

    # Test the endpoint
    response = client.get('/regular/song-details/1')
    assert response.status_code == 500
    assert response.json == {"error": "Internal error"}
