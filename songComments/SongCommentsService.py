# import pathlib

import os
# import connexion
from flask import Flask, request, jsonify, render_template
import grpc
# from grpc_interceptor import ExceptionToStatusInterceptor
# from flask import abort, make_response
# from flask_marshmallow import Marshmallow
from songComments_pb2 import (
    AddCommentRequest,
    AddCommentResponse,
    UpdateCommentRequest,
    UpdateCommentResponse,
    RemoveCommentRequest,
    RemoveCommentResponse
)
import songComments_pb2_grpc


# basedir = pathlib.Path(__file__).parent.resolve()
# connex_app = connexion.App(__name__, specification_dir=basedir)
app = Flask(__name__)

songComments_host = os.getenv("COMMENTS_HOST", "localhost")
songComments_channel = grpc.insecure_channel(f"{songComments_host}:50051")
songComments_client = songComments_pb2_grpc.CommentServiceStub(songComments_channel)

# app = config.connex_app

@app.route("/")
def render_homepage():
    return "Song Comments"

# Endpoint to add Comments to Songs
@app.route("/premium/song-details/<int:song_id>/comment", methods=["POST"])
def addComment(song_id):
    # Get the comment data from the request body
    user_id = request.form.get("user_id")
    comment = request.form.get("comment")

    print("User_id = ", user_id)
    print("Comment = ", comment)

    #grpc
    comment_request = AddCommentRequest(user_id = (user_id), song_id = song_id, comment = comment)
    comment_response = songComments_client.Add(comment_request)

    if comment_response.response == -1:
        return("ERROR, Add failed") 
    return jsonify(comment_response.response)
    

# Endpoint to update an existing comment
@app.route("/premium/song-details/<int:song_id>/comment/<int:comment_id>", methods=["PUT"])
def updateComment(song_id, comment_id):

    # Get the comment data from the request body
    user_id = request.form.get("user_id")
    comment = request.form.get("comment")

    print("User_id = ", user_id)
    print("Comment = ", comment)

    #grpc
    comment_request = UpdateCommentRequest(user_id = int(user_id), song_id = song_id, comment_id = int(comment_id), comment = comment)
    comment_response = songComments_client.Update(comment_request)

    if comment_response.response == -1:
        return("ERROR, Update failed") 
    return jsonify(comment_response.response)

# Endpoint to delete an existing comment
@app.route("/premium/song-details/<int:song_id>/comment/<int:comment_id>", methods=["DELETE"])
def deleteComment(song_id, comment_id):

    # Get the comment data from the request body
    user_id = request.form.get("user_id")

    print("User_id = ", user_id)
    #grpc
    comment_request = RemoveCommentRequest(user_id = int(user_id), song_id = song_id, comment_id = comment_id)
    comment_response = songComments_client.Remove(comment_request)

    if comment_response.response == -1:
        return("ERROR, Delete failed") 
    return jsonify(comment_response.response)

# if __name__ == "__main__":
#     app.run(debug=True)
