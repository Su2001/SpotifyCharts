# import pathlib
import os
# import connexion
from flask import Flask, session, abort, redirect, request
import grpc
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

from songComments_pb2 import (
    AddCommentRequest,
    AddCommentResponse,
    UpdateCommentRequest,
    UpdateCommentResponse,
    RemoveCommentRequest,
    RemoveCommentResponse
)
import songComments_pb2_grpc


app = Flask(__name__)

songComments_host = os.getenv("COMMENTS_HOST", "localhost")
songComments_channel = grpc.insecure_channel(f"{songComments_host}:50051")
songComments_client = songComments_pb2_grpc.CommentServiceStub(songComments_channel)


app.secret_key = "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" 

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "475938769974-0u2gdtmtdum1hhocg0qvmnbduu5b3skd.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://5000-cs-314474093647-default.cs-europe-west1-xedi.cloudshell.dev/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/premium")

@app.route("/")
def index():
    return "<a href='/login'><button>Login</button></a>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/premium")
@login_is_required
def protected_area():
    return f"Hello {session['name']}! You are logged in! <br/> <a href='/logout'><button>Logout</button></a>"

# Endpoint to add Comments to Songs
@app.route("/premium/song-details/<int:song_id>/comment", methods=["POST"])
def addComment(song_id):
    # Get the comment data from the request body
    user_id = request.args.get("user_id")
    comment = request.args.get("comment")

    print("User_id = ", user_id)
    print("Comment = ", comment)

    #grpc
    comment_request = AddCommentRequest(user_id = int(user_id), song_id = song_id, comment = comment)
    comment_response = songComments_client.Add(comment_request)

    if comment_response.response == -1:
        return("ERROR, Add failed") 
    return jsonify(comment_response.response)
    

# Endpoint to update an existing comment
@app.route("/premium/song-details/<int:song_id>/comment/<int:comment_id>", methods=["PUT"])
def updateComment(song_id, comment_id):

    # Get the comment data from the request body
    user_id = request.args.get("user_id")
    comment = request.args.get("comment")

    print("User_id = ", user_id)
    print("Comment = ", comment)

    #grpc
    comment_request = UpdateCommentRequest(user_id = int(user_id), song_id = song_id, comment_id = comment_id, comment = comment)
    comment_response = songComments_client.Update(comment_request)

    if comment_response.response == -1:
        return("ERROR, Update failed") 
    return jsonify(comment_response.response)

# Endpoint to delete an existing comment
@app.route("/premium/song-details/<int:song_id>/comment/<int:comment_id>", methods=["DELETE"])
def deleteComment(song_id, comment_id):

    # Get the comment data from the request body
    user_id = request.args.get("user_id")

    print("User_id = ", user_id)
    #grpc
    comment_request = RemoveCommentRequest(user_id = int(user_id), song_id = song_id, comment_id = comment_id)
    comment_response = songComments_client.Remove(comment_request)

    if comment_response.response == -1:
        return("ERROR, Delete failed") 
    return jsonify(comment_response.response)

# if __name__ == "__main__":
#     app.run(debug=True)
