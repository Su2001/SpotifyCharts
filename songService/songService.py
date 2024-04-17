from concurrent import futures

from flask import Flask, render_template
import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
import search_pb2
import search_pb2_grpc
import songComments_pb2_grpc
import songDetails_pb2_grpc
import socket
import pymysql
import sqlalchemy
from google.cloud.sql.connector import Connector

from songComments_pb2 import (
    AddCommentResponse,
    UpdateCommentResponse,
    RemoveCommentResponse
)

from songDetails_pb2 import (
    GetSongDetailsResponse,
    SongDetail,
    Comment
)

from health_pb2 import(
    HealthCheckRequest,
    HealthCheckResponse
)
import health_pb2_grpc
from threading import Lock

counter = 0
MAX = 10
lock = Lock()

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

class Search(search_pb2_grpc.SearchServicer):
    def GetSearch(self, request, context):
        
        def init_connection_pool(connector: Connector) -> sqlalchemy.engine.Engine:
            def getconn() -> pymysql.connections.Connection:
                conn = connector.connect(
                    "spotifychartsgroup01:europe-west4:spotifychartsgroup01database",
                    "pymysql",
                    user="root",
                    password="1234",
                    db="nonduplicatesongsdatabase"
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
        lock.acquire()
        counter = counter + 1
        lock.release()
        

        with Connector() as connector:
            pool = init_connection_pool(connector)
            with pool.connect() as db_conn:
                query = sqlalchemy.text("SELECT song_id, title, artist FROM Songs WHERE title LIKE :input LIMIT 100")
                search_term = '%' + request.songname + '%'

                # Execute the query with the search_term parameter
                result = db_conn.execute(query, {"input": search_term}).fetchall()
                songs = []
                for row in result:
                    song = search_pb2.Song(
                        id=row[0],
                        title=row[1],
                        artists=row[2]
                    )
                    songs.append(song)
        lock.acquire()
        counter = counter - 1
        lock.release()
        return search_pb2.GetSearchResponse(songs=songs)

class CommentService(songComments_pb2_grpc.CommentServiceServicer):
    def Add(self, request, context):
        def init_connection_pool(connector: Connector) -> sqlalchemy.engine.Engine:
            def getconn() -> pymysql.connections.Connection:
                conn = connector.connect(
                    "spotifychartsgroup01:europe-west4:spotifychartsgroup01database",
                    "pymysql",
                    user="root",
                    password="1234",
                    db="nonduplicatesongsdatabase"
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
        lock.acquire()
        counter = counter + 1
        lock.release()
        
        with Connector() as connector:
            pool = init_connection_pool(connector)
            with pool.connect() as db_conn:
                query = sqlalchemy.text("INSERT INTO Comments (user_id, song_id, comment) VALUES (:user_id, :song_id, :comment)")

                db_conn.execute(query, {"user_id": request.user_id,"song_id": request.song_id,"comment": request.comment})
                db_conn.commit()
            
                print("Inserted comment: ", request.user_id, request.song_id, request.comment)


        lock.acquire()
        counter = counter - 1
        lock.release()
        return AddCommentResponse(response=1)

    def Update(self, request, context):
        def init_connection_pool(connector: Connector) -> sqlalchemy.engine.Engine:
            def getconn() -> pymysql.connections.Connection:
                conn = connector.connect(
                    "spotifychartsgroup01:europe-west4:spotifychartsgroup01database",
                    "pymysql",
                    user="root",
                    password="1234",
                    db="nonduplicatesongsdatabase"
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
        lock.acquire()
        counter = counter + 1
        lock.release()
        
        with Connector() as connector:
            pool = init_connection_pool(connector)
            with pool.connect() as db_conn:
                query = sqlalchemy.text("UPDATE Comments SET comment = :comment WHERE user_id = :user_id AND song_id = :song_id AND comment_id = :comment_id")
                
                # Execute the query with the search_term parameter
                db_conn.execute(query, {"comment": request.comment,"user_id": request.user_id,"song_id": request.song_id, "comment_id": request.comment_id})
                db_conn.commit()
                print("Updated comment. The new comment is: ", request.comment)


        lock.acquire()
        counter = counter - 1
        lock.release()
        return UpdateCommentResponse(response=1)

    def Remove(self, request, context):
        def init_connection_pool(connector: Connector) -> sqlalchemy.engine.Engine:
            def getconn() -> pymysql.connections.Connection:
                conn = connector.connect(
                    "spotifychartsgroup01:europe-west4:spotifychartsgroup01database",
                    "pymysql",
                    user="root",
                    password="1234",
                    db="nonduplicatesongsdatabase"
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
        lock.acquire()
        counter = counter + 1
        lock.release()

        with Connector() as connector:
            pool = init_connection_pool(connector)
            with pool.connect() as db_conn:
                query = sqlalchemy.text("DELETE FROM Comments WHERE user_id = :user_id AND song_id = :song_id AND comment_id = :comment_id")
                
                # Execute the query with the search_term parameter
                db_conn.execute(query, {"user_id": request.user_id,"song_id": request.song_id, "comment_id": request.comment_id})
                db_conn.commit()
                print("Removed comment for user", request.user_id, "and song", request.song_id)


        lock.acquire()
        counter = counter - 1
        lock.release()
        return RemoveCommentResponse(response=1)

class SongDetails(songDetails_pb2_grpc.SongDetailsServicer):

    def GetSongDetails(self, request, context):
        def init_connection_pool(connector: Connector) -> sqlalchemy.engine.Engine:
            def getconn() -> pymysql.connections.Connection:
                conn = connector.connect(
                    "spotifychartsgroup01:europe-west4:spotifychartsgroup01database",
                    "pymysql",
                    user="root",
                    password="1234",
                    db="nonduplicatesongsdatabase"
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
        lock.acquire()
        counter = counter + 1
        lock.release()


        with Connector() as connector:
            pool = init_connection_pool(connector)
            with pool.connect() as db_conn:
                query = sqlalchemy.text("SELECT * FROM Songs WHERE song_id = :song_id")

                song_result = db_conn.execute(query, {"song_id": request.id}).fetchone()

                if song_result is None:
                    return GetSongDetailsResponse()

                song_id, title, artists, url, numtimesincharts, numcountrydif = song_result

                query = sqlalchemy.text("SELECT * FROM Comments WHERE song_id = :song_id2")
                
                comment_results = db_conn.execute(query, {"song_id2": request.id}).fetchall()

                comments = []
                for comment_result in comment_results:
                    comment_id, user_id, song_id, comment_text = comment_result
                    comments.append(Comment(comment_id=comment_id, user_id=user_id, song_id=song_id, comment=comment_text))

                song = SongDetail(song_id=song_id, title=title, artists=artists, url=url, numtimesincharts=numtimesincharts, numcountrydif=numcountrydif, comments=comments)

        lock.acquire()
        counter = counter - 1
        lock.release()
        return GetSongDetailsResponse(song=song)


def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    search_pb2_grpc.add_SearchServicer_to_server(
        Search(), server
    )
    songComments_pb2_grpc.add_CommentServiceServicer_to_server(
        CommentService(), server 
    )
    songDetails_pb2_grpc.add_SongDetailsServicer_to_server(
        SongDetails(), server 
    )
    health_pb2_grpc.add_HealthServicer_to_server(
        HealthCheck(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
    
if __name__ == "__main__":
    serve()
