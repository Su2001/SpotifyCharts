from flask import Flask, session, abort, redirect, request, jsonify
import os
from playlist_pb2 import ModifyPlayListRequest, GetPlayListRequest
from playlist_pb2_grpc import PlayListServiceStub
import grpc
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests


playList_host = os.getenv("USERSERVICE_HOST", "localhost")
playList_channel = grpc.insecure_channel(f"{playList_host}:50051")
playList_client = PlayListServiceStub(playList_channel)

app = Flask(__name__)
app.secret_key = "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" # certifique-se de que isso corresponda ao que está em client_secret.json

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # permitir tráfego HTTP para desenvolvimento local

GOOGLE_CLIENT_ID = "475938769974-0u2gdtmtdum1hhocg0qvmnbduu5b3skd.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://8080-cs-314474093647-default.cs-europe-west1-xedi.cloudshell.dev/callback"
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
    return redirect("/premium/playlist")

@app.route("/")
def index():
    return "<a href='/login'><button>Login</button></a>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/health")
def healthCheck():
    return jsonify("ok")

@app.route("/premium/playlist", methods=["GET"])
@login_is_required
def get_PlayList():
    user_id = request.args.get("user_id")
    #grpc
    requestAux = GetPlayListRequest(user_id=int(user_id))
    response = playList_client.Get(requestAux)
    if response.response == -1:
        return ("ERROR, the user is not found") 
    a = list(response.songs)
    return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>" + jsonify(a)
    """
    if sucess :
        return 
    else:
        abort(404, f"playList with ID {user_id} not found")
    """

@app.route("/premium/playlist/<int:song_id>", methods=["POST"])
# @login_is_required
def add_PlayList(song_id):
    user_id = str(request.json.get("user_id"))

    #grpc
    requestAux = ModifyPlayListRequest(user_id = int(user_id), song_id = song_id)
    response = playList_client.Add(requestAux)
    if response.response == -1:
        return("ERROR, Add failed") 
    return jsonify("Add success")

@app.route("/premium/playlist/<int:song_id>", methods=["DELETE"])
# @login_is_required
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