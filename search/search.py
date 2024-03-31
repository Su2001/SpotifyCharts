from flask import Flask, request, render_template, jsonify
import os
import grpc
import search_pb2
import search_pb2_grpc
app = Flask(__name__)

search_host = os.getenv("TOPCHARTS_HOST", "localhost")
search_channel = grpc.insecure_channel(f"{search_host}:50051")
search_client = search_pb2_grpc.SearchStub(search_channel)

def song_to_dict(song):
    return {
        "id": song.id,
        "title": song.title,
        "artists": song.artists
    }

@app.route("/")
def render_homepage():
    return "Home"

@app.route("/regular/search")
def search():
    songAux = request.args.get("song")        #maybe no futuro arranjar valores default para isto
    
    if songAux:
        search_request = search_pb2.GetSearchRequest(songname=songAux)
        search_response = search_client.GetSearch(search_request)
        if len(search_response.songs) > 0:
            response_dict = {
                "songs": [song_to_dict(song) for song in search_response.songs]
            }
            return jsonify(response_dict)
        else:
            return("ERROR, NO MATCH")

    return("ERROR ON INPUT")


if __name__ == "__main__":
    app.run(debug = True)


