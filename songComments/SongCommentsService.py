import pathlib

import connexion
from flask import abort, make_response
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

songComments_host = os.getenv("COMMENTS_HOST", "localhost")
songComments_channel = grpc.insecure_channel(f"{songComments_host}:50051")
songComments_client = songComments_pb2_grpc.CommentServiceStub(songComments_channel)

app = config.connex_app

# Endpoint to add Comments to Songs
@app.route("/premium/song-details/{song_id}/comment", methods=["POST"])
def addComment(song_id):
    # Get the comment data from the request body
    user_id = request.args.get("user_id")
    comment = request.args.get("comment")

    print("User_id = ", user_id)
    print("Comment = ", comment)

    #grpc
    request = AddCommentRequest(user_id = user_id, song_id = song_id, comment = comment)
    response = songComments_client.Add(request)

    if response.response == -1:
        return("ERROR, Add failed") 
    return jsonify(response)
    

# Endpoint to update an existing comment
@app.route("/premium/song-details/{song_id}/comment/{comment_id}", methods=["PUT"])
def updateComment(song_id, comment_id):

    # Get the comment data from the request body
    user_id = request.args.get("user_id")
    comment = request.args.get("comment")

    print("User_id = ", user_id)
    print("Comment = ", comment)

    #grpc
    request = UpdateCommentRequest(user_id = user_id, song_id = song_id, comment_id = comment_id, comment = comment)
    response = songComments_client.Update(request)

    if response.response == -1:
        return("ERROR, Update failed") 
    return jsonify(response)

# Endpoint to delete an existing comment
@app.route("/premium/song-details/{song_id}/comment/{comment_id}", methods=["DELETE"])
def deleteComment(comment_id):

    # Get the comment data from the request body
    user_id = request.args.get("user_id")

    print("User_id = ", user_id)
    #grpc
    request = RemoveCommentRequest(user_id = user_id, song_id = song_id, comment_id = comment_id)
    response = songComments_client.Remove(request)

    if response.response == -1:
        return("ERROR, Delete failed") 
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
