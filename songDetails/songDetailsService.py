from flask import Flask, request, jsonify, render_template
import os
import songDetails_pb2
import songDetails_pb2_grpc
import grpc
import random
import time
from flask import Flask

app = Flask(__name__)

songDetails_host = os.getenv("SONGDETAILS_HOST", "localhost")
songDetails_channel = grpc.insecure_channel(f"{songDetails_host}:50051")
songDetails_client = songDetails_pb2_grpc.SongDetailsStub(songDetails_channel)

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
    PYTHON_REQUESTS_COUNTER.inc()
    return "Song Details"

@app.route("/regular/song-details/<int:song_id>", methods=["GET"])
def song_details(song_id):
    request = songDetails_pb2.GetSongDetailsRequest(id=song_id)
    response = songDetails_client.GetSongDetails(request)
    song = song_to_dict(response.song)
    return jsonify(song)

# if __name__ == "__main__":
#     app.run(debug=True)