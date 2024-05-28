from flask import Flask, request, jsonify, render_template
import os
import topCharts_pb2
import topCharts_pb2_grpc
import grpc
import time
from prometheus_client import Counter, Histogram, generate_latest

app = Flask(__name__)

topCharts_host = os.getenv("TOPCHARTS_HOST", "localhost")
topCharts_channel = grpc.insecure_channel(f"{topCharts_host}:50051")
topCharts_client = topCharts_pb2_grpc.TopChartsStub(topCharts_channel)
REQUEST_COUNT = Counter('topchars_requests_total', 'Total number of requests to /regular/top-charts')
FAILURES_COUNT = Counter('topchars_failures_total', 'Total number of failures to /regular/top-charts')
REQUEST_LATENCY = Histogram('topchars_request_latency_seconds', 'Latency of requests to /regular/top-charts')


def song_to_dict(song):
    return {
        "id": song.id,
        "title": song.title,
        "artists": song.artists,
        "rank": song.rank,
        "chart": song.chart
    }

@app.route("/")
def deafaut():
    return jsonify("TopChart")

@app.route("/health")
def healthCheck():
    return jsonify("ok")

@app.route("/regular/top-charts")
def render_homepage():
    REQUEST_COUNT.inc()  # Increment the request count
    start_time = time.time()  # Start the timer

    dateAux = request.args.get("date")
    countryAux = request.args.get("country")

    if dateAux and countryAux:
        topCharts_request = topCharts_pb2.GetTopChartsRequest(
            date=dateAux, country=countryAux)
      
        topCharts_response = topCharts_client.GetTopCharts(topCharts_request)
        if len(topCharts_response.songs) > 0:
            response_dict = {
                "songs": [song_to_dict(song) for song in topCharts_response.songs]
            }
            
            REQUEST_LATENCY.observe(time.time() - start_time)
            return jsonify(response_dict)
        else:
            FAILURES_COUNT.inc()
            REQUEST_LATENCY.observe(time.time() - start_time)
            return("ERROR, NO MATCH FOR THE COUNTRY AND DATE INPUTED")
    FAILURES_COUNT.inc()
    REQUEST_LATENCY.observe(time.time() - start_time)
    return "ERROR, YOU HAVE TO INPUT A DATE AND A COUNTRY, SYNTAX FOR THE DATE- '%Y-%m-%d' "

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == "__main__":
    app.run(debug=True)
