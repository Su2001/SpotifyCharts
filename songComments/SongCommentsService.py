# import pathlib
import os
# import connexion
from flask import Flask, session, abort, redirect, request, jsonify
import grpc
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import time
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




flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://34.120.107.89/callback"
)

REQUEST_COUNT = Counter('song_comments_requests_total', 'Total number of requests')
FAILURES_COUNT = Counter('song_comments_failures_total', 'Total number of requests')
REQUEST_LATENCY = Histogram('song_comments_request_latency_seconds', 'Latency of requests')
AUTH_REQUEST_COUNT = Counter('song_comments_auth_requests_total', 'Total number of authentication requests')
SUCESSEFULL_AUTH_REQUEST_COUNT = Counter('song_comments_sucessfull_auth_requests_total', 'Total number of authentication requests')


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

@app.route("/premium/song-details/auxlogin")
def login():
    AUTH_REQUEST_COUNT.inc()
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/premium/song-details/callback")
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
    SUCESSEFULL_AUTH_REQUEST_COUNT.inc()
    return redirect("/premium")

@app.route("/premium/song-details/login")
def index():
    return "<a href='/premium/song-details/auxlogin'><button>Login</button></a>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/health")
def healthCheck():
    return jsonify("ok")

@app.route("/")
def non():
    return jsonify("ok")

@app.route("/premium")
@login_is_required
def protected_area():
    return f"Hello {session['name']}! You are logged in! <br/> <a href='/logout'><button>Logout</button></a>"

# Endpoint to add Comments to Songs
@app.route("/premium/song-details/<int:song_id>/comment", methods=["POST"])
def addComment(song_id):
    REQUEST_COUNT.inc() 
    start_time = time.time() 
    # Get the comment data from the request body
    user_id = request.args.get("user_id")
    comment = request.args.get("comment")

    print("User_id = ", user_id)
    print("Comment = ", comment)

    #grpc
    comment_request = AddCommentRequest(user_id = int(user_id), song_id = song_id, comment = comment)
    comment_response = songComments_client.Add(comment_request)

    if comment_response.response == -1:
        FAILURES_COUNT.inc()
        REQUEST_LATENCY.observe(time.time() - start_time)
        return("ERROR, Add failed") 
    REQUEST_LATENCY.observe(time.time() - start_time)
    return jsonify(comment_response.response)
    

# Endpoint to update an existing comment
@app.route("/premium/song-details/<int:song_id>/comment/<int:comment_id>", methods=["PUT"])
def updateComment(song_id, comment_id):
    REQUEST_COUNT.inc()
    start_time = time.time()
    # Get the comment data from the request body
    user_id = request.args.get("user_id")
    comment = request.args.get("comment")

    print("User_id = ", user_id)
    print("Comment = ", comment)

    #grpc
    comment_request = UpdateCommentRequest(user_id = int(user_id), song_id = song_id, comment_id = comment_id, comment = comment)
    comment_response = songComments_client.Update(comment_request)

    if comment_response.response == -1:
        FAILURES_COUNT.inc()
        REQUEST_LATENCY.observe(time.time() - start_time)
        return("ERROR, Update failed") 
    REQUEST_LATENCY.observe(time.time() - start_time)
    return jsonify(comment_response.response)

@app.route("/metrics", methods=["GET"])
def stats():
    return generate_latest()

# Endpoint to delete an existing comment
@app.route("/premium/song-details/<int:song_id>/comment/<int:comment_id>", methods=["DELETE"])
def deleteComment(song_id, comment_id):
    REQUEST_COUNT.inc()
    start_time = time.time()
    # Get the comment data from the request body
    user_id = request.args.get("user_id")

    print("User_id = ", user_id)
    #grpc
    comment_request = RemoveCommentRequest(user_id = int(user_id), song_id = song_id, comment_id = comment_id)
    comment_response = songComments_client.Remove(comment_request)

    if comment_response.response == -1:
        FAILURES_COUNT.inc()
        REQUEST_LATENCY.observe(time.time() - start_time)
        return("ERROR, Delete failed")
    REQUEST_LATENCY.observe(time.time() - start_time) 
    return jsonify(comment_response.response)

# if __name__ == "__main__":
#     app.run(debug=True)
