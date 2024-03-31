import pathlib

import connexion
from flask import abort, make_response
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = config.connex_app

# Endpoint to add Comments to Songs
@app.route("/premium/song-details/{song_id}/comment", methods=["POST"])
def addComment(song_id):
    # Obter os dados do comentário do corpo da solicitação
    data = request.json
    
    # Lógica para adicionar o comentário à música com o ID song_id

    return jsonify({"message": "Comment added successfully"}), 201

# Endpoint to update an existing comment
@app.route("/premium/song-details/{song_id}/comment/{comment_id}", methods=["PUT"])
def updateComment(song_id, comment_id):
    # Obter os novos dados do comentário do corpo da requisição
    data = request.json
    
    # Lógica para atualizar o comentário com o ID comment_id

    return jsonify({"message": "Comment updated successfully"}), 200

# Endpoint to delete an existing comment
@app.route("/premium/song-details/{song_id}/comment/{comment_id}", methods=["DELETE"])
def deleteComment(comment_id):
    # Lógica para excluir o comentário com o ID comment_id

    return jsonify({"message": "Comment deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)