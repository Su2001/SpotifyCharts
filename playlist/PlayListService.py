from flask import Flask, request, jsonify, render_template
import os
from playlist_pb2 import AddPlayListRequest, GetPlayListRequest, RemovePlayListRequest
from playlist_pb2_grpc import AddPlayListStub, GetPlayListStub, RemovePlayListStub
import grpc

app = Flask(__name__)

playList_host = os.getenv("PLAYLIST_HOST", "localhost")
playList_channel = grpc.insecure_channel(f"{playList_host}:50051")
post_playList_client = AddPlayListStub(playList_channel)
delete_playList_client = RemovePlayListStub(playList_channel)
get_playList_client = GetPlayListStub(playList_channel)

@app.route("/")
@app.route("/premium/playlist", methods=["GET"])
def get_PlayList():
    user_id = request.args.get("user_id")
    #grpc
    request = GetPlayListRequest(user_id=user_id)
    response = get_playList_client.Get(request)
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
    print(123)
    #grpc
    request = AddPlayListRequest(user_id = user_id, song_id = song_id)
    response = post_playList_client.Add(request)
    if response.response == -1:
        return("ERROR, Add failed") 
    return jsonify(response)

@app.route("/premium/playlist/<int:song_id>", methods=["DELETE"])
def remove_PlayList(song_id):
    user_id = request.args.get("user_id")
    print(123)
    #grpc
    request = RemovePlayListRequest(user_id = user_id, song_id = song_id)
    response = delete_playList_client.Remove(request)
    if response.response == -1:
        return("ERROR, Remove failed") 
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)