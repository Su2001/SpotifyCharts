from flask import Flask, request, jsonify, render_template
import os
from playlist_pb2 import ModifyPlayListRequest, GetPlayListRequest
from playlist_pb2_grpc import PlayListServiceStub
import grpc

app = Flask(__name__)

playList_host = os.getenv("PLAYLIST_HOST", "localhost")
playList_channel = grpc.insecure_channel(f"{playList_host}:50051")
playList_client = PlayListServiceStub(playList_channel)

@app.route("/")
@app.route("/premium/playlist", methods=["GET"])
def get_PlayList():
    user_id = request.args.get("user_id")
    #grpc
    request = GetPlayListRequest(user_id=user_id)
    response = playList_client.Get(request)
    if response.response == -1:
        return ("ERROR, the user is not found") 
    a = list(response.songs)
    return jsonify(a)
    """
    if sucess :
        return 
    else:
        abort(404, f"playList with ID {user_id} not found")
    """

@app.route("/premium/playlist/<int:song_id>", methods=["POST"])
def add_PlayList(song_id):
    user_id = request.args.get("user_id")

    #grpc
    request = ModifyPlayListRequest(user_id = user_id, song_id = song_id)
    response = playList_client.Add(request)
    if response.response == -1:
        return("ERROR, Add failed") 
    return jsonify(response)

@app.route("/premium/playlist/<int:song_id>", methods=["DELETE"])
def remove_PlayList(song_id):
    user_id = request.args.get("user_id")

    #grpc
    request = ModifyPlayListRequest(user_id = user_id, song_id = song_id)
    response = playList_client.Remove(request)
    if response.response == -1:
        return("ERROR, Remove failed") 
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)