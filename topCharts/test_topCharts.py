import pytest
import warnings

# Suppress specific warning types
warnings.filterwarnings("ignore", category=DeprecationWarning)
from unittest.mock import patch
import sys

# Add the path to the directory containing topCharts_pb2.py
sys.path.append('.')  # Adjust the path as per your directory structure

# Import topCharts_pb2 from the correct location
from topCharts_pb2 import GetTopChartsResponse

# Import the Flask app instance from topCharts.py
from topCharts import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == "ok"

def test_default_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == "TopChart"

@patch('topCharts.topCharts_client.GetTopCharts')
def test_render_homepage_success(mock_get_top_charts, client):
    # Mock gRPC response
    mock_response = GetTopChartsResponse()
    song = mock_response.songs.add()
    song.id = 1
    song.title = "Test Song"
    song.artists = "Test Artist"
    song.rank = 1
    song.chart = "Test Chart"
    
    mock_get_top_charts.return_value = mock_response

    # Test the endpoint with valid parameters
    response = client.get('/regular/top-charts?date=2024-01-01&country=US')
    assert response.status_code == 200
    assert response.json == {
        "songs": [
            {
                "id": 1,
                "title": "Test Song",
                "artists": "Test Artist",
                "rank": 1,
                "chart": "Test Chart"
            }
        ]
    }

@patch('topCharts.topCharts_client.GetTopCharts')
def test_render_homepage_no_match(mock_get_top_charts, client):
    # Mock gRPC response with no songs
    mock_response = GetTopChartsResponse()
    mock_get_top_charts.return_value = mock_response

    # Test the endpoint with valid parameters but no matches
    response = client.get('/regular/top-charts?date=2020-01-01&country=Argentina')
    assert response.status_code == 200
    assert response.data.decode() == "ERROR, NO MATCH FOR THE COUNTRY AND DATE INPUTED"

def test_render_homepage_missing_parameters(client):
    # Test the endpoint with missing parameters
    response = client.get('/regular/top-charts')
    assert response.status_code == 200
    assert response.data.decode() == "ERROR, YOU HAVE TO INPUT A DATE AND A COUNTRY, SYNTAX FOR THE DATE- '%Y-%m-%d' "
