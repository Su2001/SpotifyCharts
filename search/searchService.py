from flask import Flask, request, render_template, jsonify
import os
import grpc
import search_pb2
import search_pb2_grpc
from prometheus_client import Counter, Histogram, generate_latest
import time

app = Flask(__name__)

search_host = os.getenv("SEARCH_HOST", "localhost")
search_channel = grpc.insecure_channel(f"{search_host}:50051")
search_client = search_pb2_grpc.SearchStub(search_channel)

REQUEST_COUNT = Counter('search_requests_total', 'Total number of requests to /regular/search')
FAILURES_COUNT = Counter('search_failures_total', 'Total number of requests to /regular/search')
REQUEST_LATENCY = Histogram('search_request_latency_seconds', 'Latency of requests to /regular/search')

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
    REQUEST_COUNT.inc()
    start_time = time.time() 
    songAux = request.args.get("song")      
    
    if songAux:
        search_request = search_pb2.GetSearchRequest(songname=songAux)
        search_response = search_client.GetSearch(search_request)
        if len(search_response.songs) > 0:
            response_dict = {
                "songs": [song_to_dict(song) for song in search_response.songs]
            }
            
            REQUEST_LATENCY.observe(time.time() - start_time) 
            return jsonify(response_dict)
        else:
            FAILURES_COUNT.inc()
            REQUEST_LATENCY.observe(time.time() - start_time)
            return("ERROR, NO MATCH")
    FAILURES_COUNT.inc()
    REQUEST_LATENCY.observe(time.time() - start_time)   
    return("ERROR ON INPUT")

@app.route('/regular/search/metrics')
def metrics():
    return generate_latest()

# if __name__ == "__main__":
#     app.run(debug = True)


