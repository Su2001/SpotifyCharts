from concurrent import futures
import random

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
import mysql.connector

from playlist_pb2 import(
    ModifyPlayListRequest,
    GetPlayListRequest,
    GetPlayListResponse,
    PlayListResponse
)

import playlist_pb2_grpc

mydb = mysql.connector.connect(
    host="172.18.0.2",
    user="root",
    password="1234"
)
mycursor = mydb.cursor()
mydb.database = "usersdatabase"

class PlayListService(playlist_pb2_grpc.PlayListServiceServicer):
    def Add(self, request, context):
        #interacte bd
        try:
            query = "INSERT INTO usersdatabase.playlists (user_id, song_id) VALUES (%d, %d);"
            mycursor.execute(query, (request.user_id, request.song_id,))
        except:
            return PlayListResponse(response=-1)
        
        print("Inserted comment: ", request.user_id, request.song_id)
        return PlayListResponse(response=1)

    def Remove(self, request, context):
        #interacte bd
        try:
            query = "DELETE FROM usersdatabase.playlists WHERE user_id = %d AND song_id = %d;"
            mycursor.execute(query, (request.user_id, request.song_id,))
        except:
            return PlayListResponse(response=-1)
        print("Removed a song for user", request.user_id, "and song", request.song_id)
        return PlayListResponse(response=1)

    def Get(self, request, context):
        #interacte bd
        try:
            query = "SELECT song_id FROM usersdatabase.playlists WHERE user_id = %d;"
            select_term = '%' + request.song_id + '%'  
            mycursor.execute(query, (select_term,))
            result = mycursor.fetchall()
            return GetPlayListResponse(response = 1,songs=result) 
        except:
            return GetPlayListResponse(response = -1,songs=[]) 
           

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    playlist_pb2_grpc.add_PlayListServiceServicer_to_server(
        PlayListService(), server
    )
    """
    with open("server.key", "rb") as fp:
        server_key = fp.read()
    with open("server.pem", "rb") as fp:
        server_cert = fp.read()
    with open("ca.pem", "rb") as fp:
        ca_cert = fp.read()
    
    creds = grpc.ssl_server_credentials(
        [(server_key, server_cert)],
        root_certificates=ca_cert,
        require_client_auth=True,
    )
    """

    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()