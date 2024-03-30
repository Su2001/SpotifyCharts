import pathlib

import connexion
from flask import abort, make_response
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = config.connex_app

@app.route("/premium/playlist", methods=["GET"])
def get_PlayList(user):
    user_id = user.get("user_id")

    #grpc

    """
    if sucess :
        return 
    else:
        abort(404, f"playList with ID {user_id} not found")
    """

@app.route("/premium/playlist/{song_id}", methods=["POST"])
def add_PlayList(song_id, user):
    pass

@app.route("/premium/playlist/{song_id}", methods=["DELETE"])
def remove_PlayList(song_id, user):
    pass