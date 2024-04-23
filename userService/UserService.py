from concurrent import futures
import random

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from google.cloud.sql.connector import Connector
import pymysql
import sqlalchemy

from playlist_pb2 import(
    ModifyPlayListRequest,
    GetPlayListRequest,
    GetPlayListResponse,
    PlayListResponse
)
from health_pb2 import(
    HealthCheckRequest,
    HealthCheckResponse
)
from threading import Lock

import playlist_pb2_grpc
import health_pb2_grpc
import socket
from google.oauth2 import service_account
import json, os

counter = 0
MAX = 10
lock = Lock()
f = open(os.getenv("AUTH_JSON")+".json")
json_file = json.load(f)
credentials = service_account.Credentials.from_service_account_info(json_file)
f.close()
class HealthCheck(health_pb2_grpc.HealthServicer):

    def Check(self, request, context):
        global MAX
        global counter
        print("check")
        if counter < MAX:
            return HealthCheckResponse(status=1)
        if counter == MAX:
            return HealthCheckResponse(status=2)

    def Watch(self, request, context):
        pass

class PlayListService(playlist_pb2_grpc.PlayListServiceServicer):
    def Add(self, request, context):
        
        def init_connection_pool(connector: Connector) -> sqlalchemy.engine.Engine:
            def getconn() -> pymysql.connections.Connection:
                conn = connector.connect(
                    "spotifychartsgroup01:europe-west4:spotifychartsgroup01database",
                    "pymysql",
                    user="root",
                    password="1234",
                    db="usersdatabase"
                )
                return conn
            pool = sqlalchemy.create_engine(
                "mysql+pymysql://",
                creator=getconn,
            )
            return pool
        global MAX
        global counter
        global lock
        global credentials
        lock.acquire()
        counter = counter + 1
        lock.release()

        with Connector(credentials=credentials) as connector:
            pool = init_connection_pool(connector)
            with pool.connect() as db_conn:
                query = sqlalchemy.text(
                "INSERT INTO playlists (user_id, song_id) VALUES (:user_id, :song_id)")
                db_conn.execute(query,{"user_id": request.user_id, "song_id": request.song_id})
                db_conn.commit()
                db_conn.close()
        lock.acquire()
        counter = counter - 1
        lock.release()
        return PlayListResponse(response=1)

    def Remove(self, request, context):
        def init_connection_pool(connector: Connector) -> sqlalchemy.engine.Engine:
            def getconn() -> pymysql.connections.Connection:
                conn = connector.connect(
                    "spotifychartsgroup01:europe-west4:spotifychartsgroup01database",
                    "pymysql",
                    user="root",
                    password="1234",
                    db="usersdatabase"
                )
                return conn
            pool = sqlalchemy.create_engine(
                "mysql+pymysql://",
                creator=getconn,
            )
            return pool
        global MAX
        global counter
        global lock
        global credentials
        lock.acquire()
        counter = counter + 1
        lock.release()
        with Connector(credentials=credentials) as connector:
            pool = init_connection_pool(connector)
            with pool.connect() as db_conn:
                query = sqlalchemy.text(
                "DELETE FROM playlists WHERE user_id = :user_id AND song_id = :song_id")
                db_conn.execute(query,{"user_id": request.user_id, "song_id": request.song_id})
                db_conn.commit()
                db_conn.close()
        lock.acquire()
        counter = counter - 1
        lock.release()
        return PlayListResponse(response=1)

    def Get(self, request, context):
        def init_connection_pool(connector: Connector) -> sqlalchemy.engine.Engine:
            def getconn() -> pymysql.connections.Connection:
                conn = connector.connect(
                    "spotifychartsgroup01:europe-west4:spotifychartsgroup01database",
                    "pymysql",
                    user="root",
                    password="1234",
                    db="usersdatabase"
                )
                return conn
            pool = sqlalchemy.create_engine(
                "mysql+pymysql://",
                creator=getconn,
            )
            return pool
        global MAX
        global counter
        global lock
        global credentials
        print("get")
        lock.acquire()
        counter = counter + 1
        lock.release()
        with Connector(credentials=credentials) as connector:
            pool = init_connection_pool(connector)
            with pool.connect() as db_conn:
                query = sqlalchemy.text(
                "SELECT song_id FROM playlists WHERE user_id = :user_id")
                result = db_conn.execute(query,{"user_id": request.user_id}).fetchall()
                songs = []
                for row in result:
                    song = id=row[0]
                    songs.append(song)
                db_conn.close()
        lock.acquire()
        counter = counter - 1
        lock.release()
        return GetPlayListResponse(response = 1,songs=songs)
           

def serve():
    print("start serve")
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=MAX), interceptors=interceptors
    )
    playlist_pb2_grpc.add_PlayListServiceServicer_to_server(
        PlayListService(), server
    )
    health_pb2_grpc.add_HealthServicer_to_server(
        HealthCheck(), server
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