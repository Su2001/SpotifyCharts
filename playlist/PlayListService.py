from flask import Flask, request, jsonify, render_template
import os
from playlist_pb2 import ModifyPlayListRequest, GetPlayListRequest
from playlist_pb2_grpc import PlayListServiceStub
import grpc

app = Flask(__name__)

playList_host = os.getenv("USERSERVICE_HOST", "localhost")
playList_channel = grpc.insecure_channel(f"{playList_host}:50051")
playList_client = PlayListServiceStub(playList_channel)

@app.route("/", methods=["GET"])
def get_yList():
    user_id = 1
    #grpc
    requestAux = GetPlayListRequest(user_id=user_id)
    response = playList_client.Get(requestAux)
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

@app.route("/premium/playlist", methods=["GET"])
def get_PlayList():
    user_id = request.args.get("user_id")
    #grpc
    requestAux = GetPlayListRequest(user_id=int(user_id))
    response = playList_client.Get(requestAux)
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
    user_id = str(request.json.get("user_id"))

    #grpc
    requestAux = ModifyPlayListRequest(user_id = int(user_id), song_id = song_id)
    response = playList_client.Add(requestAux)
    if response.response == -1:
        return("ERROR, Add failed") 
    return jsonify("Add success")

@app.route("/premium/playlist/<int:song_id>", methods=["DELETE"])
def remove_PlayList(song_id):
    user_id = str(request.args.get("user_id"))

    #grpc
    requestAux = ModifyPlayListRequest(user_id = int(user_id), song_id = song_id)
    response = playList_client.Remove(requestAux)
    if response.response == -1:
        return("ERROR, Remove failed") 
    return jsonify("Remove success")

#if __name__ == "__main__":
 #   app.run(host="0.0.0.0", debug=True)