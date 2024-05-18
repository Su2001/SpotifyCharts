from flask import Flask, request, jsonify, render_template
import os
import topCharts_pb2
import topCharts_pb2_grpc
import grpc

app = Flask(__name__)

topCharts_host = os.getenv("TOPCHARTS_HOST", "localhost")
topCharts_channel = grpc.insecure_channel(f"{topCharts_host}:50051")
topCharts_client = topCharts_pb2_grpc.TopChartsStub(topCharts_channel)

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
            return jsonify(response_dict)
        else:
            return("ERROR, NO MATCH FOR THE COUNTRY AND DATE INPUTED")

    return "ERROR, YOU HAVE TO INPUT A DATE AND A COUNTRY, SYNTAX FOR THE DATE- '%Y-%m-%d' "

if __name__ == "__main__":
    app.run(debug=True)
