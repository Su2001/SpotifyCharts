from flask import Flask, request, jsonify, render_template
import os
import songDetails_pb2
import songDetails_pb2_grpc
import grpc
import random
import time
from flask import Flask
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY

app = Flask(__name__)

songDetails_host = os.getenv("SONGDETAILS_HOST", "localhost")
songDetails_channel = grpc.insecure_channel(f"{songDetails_host}:50051")
songDetails_client = songDetails_pb2_grpc.SongDetailsStub(songDetails_channel)


REQUEST_COUNT = Counter('songdetails_requests_total', 'Total number of requests to /regular/song-details')
FAILURES_COUNT = Counter('songdetails_failures_total', 'Total number of failures to /regular/song-details')
REQUEST_LATENCY = Histogram('songdetails_request_latency_seconds', 'Latency of requests to /regular/song-details')

cache ={}

def song_to_dict(song):
    return {
        "song_id": song.song_id,
        "title": song.title,
        "artists": song.artists,
        "url": song.url,
        "numtimesincharts": song.numtimesincharts,
        "numcountrydif": song.numcountrydif,
        "comments": [{"comment_id": comment.comment_id, "user_id": comment.user_id, "song_id": comment.song_id, "comment": comment.comment} for comment in song.comments]
    }


@app.route("/")
def render_homepage():
    return "Song Details"

@app.route("/regular/song-details/<int:song_id>", methods=["GET"])
def song_details(song_id):
    REQUEST_COUNT.inc()  
    start_time = time.time() 
    # request = songDetails_pb2.GetSongDetailsRequest(id=song_id)
    # response = songDetails_client.GetSongDetails(request)
    # song = song_to_dict(response.song)
    # return jsonify(song)
    if song_id in cache:
        return jsonify(cache[song_id])
    try:
        request = songDetails_pb2.GetSongDetailsRequest(id=song_id)
        response = songDetails_client.GetSongDetails(request)
        song = song_to_dict(response.song)
        cache[song_id] = song
        return jsonify(song)
    except Exception as e:
        FAILURES_COUNT.inc()
        app.logger.error(f"Error retrieving song details: {e}")
        return internal_error(e)
    finally:
        REQUEST_LATENCY.observe(time.time() - start_time)

@app.route("/metrics", methods=["GET"])
def stats():
    return generate_latest()
@app.errorhandler(500)
def internal_error(error):
    response = jsonify({"error": "Internal error"})
    response.status_code = 500
    return response
# if __name__ == "__main__":
#     app.run(debug=True)