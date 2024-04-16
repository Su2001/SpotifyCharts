from concurrent import futures

from flask import Flask, render_template
import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
import search_pb2
import search_pb2_grpc
import songComments_pb2_grpc
import songDetails_pb2_grpc
import socket

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

import mysql.connector

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
        # db_container_name = 'spotifychartsgroup1_db_1'
        
        # db_ip = socket.gethostbyname(db_container_name)
        global MAX
        global counter
        global lock
        lock.acquire()
        counter = counter + 1
        lock.release()
        mydb = mysql.connector.connect(
            host="34.34.73.69",
                user="root",
                password='1234'
        )
        mycursor = mydb.cursor()
        mydb.database = "nonduplicatesongsdatabase"

        query = "SELECT song_id, title, artist FROM nonduplicatesongsdatabase.Songs WHERE title LIKE %s"
        search_term = '%' + request.songname + '%'  # Assuming user_input_title is the substring provided by the user
        mycursor.execute(query, (search_term,))
        result = mycursor.fetchall()
        songs = []
        for row in result:
            song = search_pb2.Song(
                id=row[0],
                title=row[1],
                artists=row[2]
            )
            songs.append(song)
            # print("Fetched song:", song)
        mydb.close()
        lock.acquire()
        counter = counter - 1
        lock.release()
        return search_pb2.GetSearchResponse(songs=songs)

class CommentService(songComments_pb2_grpc.CommentServiceServicer):
    def Add(self, request, context):
        # db_container_name = 'spotifychartsgroup1_db_1'
        
        # db_ip = socket.gethostbyname(db_container_name)
        global MAX
        global counter
        global lock
        lock.acquire()
        counter = counter + 1
        lock.release()
        mydb = mysql.connector.connect(
            host="34.34.73.69",
                user="root",
                password='1234'
        )
        mycursor = mydb.cursor()
        mydb.database = "nonduplicatesongsdatabase"
        query = "INSERT INTO nonduplicatesongsdatabase.Comments (user_id, song_id, comment) VALUES (%s, %s, %s)"
        mycursor.execute(query, (request.user_id, request.song_id, request.comment,))
        print("Inserted comment: ", request.user_id, request.song_id, request.comment)
        mydb.commit()
        mydb.close()
        lock.acquire()
        counter = counter - 1
        lock.release()
        return AddCommentResponse(response=1)

    def Update(self, request, context):
        # db_container_name = 'spotifychartsgroup1_db_1'
       
        # db_ip = socket.gethostbyname(db_container_name)
        global MAX
        global counter
        global lock
        lock.acquire()
        counter = counter + 1
        lock.release()
        mydb = mysql.connector.connect(
            host="34.34.73.69",
                user="root",
                password='1234'
        )
        mycursor = mydb.cursor()
        mydb.database = "nonduplicatesongsdatabase"
        query = "UPDATE nonduplicatesongsdatabase.Comments SET comment = %s WHERE user_id = %s AND song_id = %s AND comment_id =%s"
        mycursor.execute(query, (request.comment, request.user_id, request.song_id,request.comment_id))
        print("Updated comment. The new comment is: ", request.comment)
        mydb.commit()
        mydb.close()
        lock.acquire()
        counter = counter - 1
        lock.release()
        return UpdateCommentResponse(response=1)

    def Remove(self, request, context):
        # db_container_name = 'spotifychartsgroup1_db_1'
       
        # db_ip = socket.gethostbyname(db_container_name)
        global MAX
        global counter
        global lock
        lock.acquire()
        counter = counter + 1
        lock.release()
        mydb = mysql.connector.connect(
            host="34.34.73.69",
                user="root",
                password='1234'
        )
        mycursor = mydb.cursor()
        mydb.database = "nonduplicatesongsdatabase"
        query = "DELETE FROM nonduplicatesongsdatabase.Comments WHERE user_id = %s AND song_id = %s AND comment_id = %s"
        mycursor.execute(query, (request.user_id, request.song_id, request.comment_id))
        print("Removed comment for user", request.user_id, "and song", request.song_id)
        mydb.commit()
        mydb.close()
        lock.acquire()
        counter = counter - 1
        lock.release()
        return RemoveCommentResponse(response=1)

class SongDetails(songDetails_pb2_grpc.SongDetailsServicer):

    def GetSongDetails(self, request, context):
        
        # db_container_name = 'spotifychartsgroup1_db_1'
  
        # db_ip = socket.gethostbyname(db_container_name)

        global MAX
        global counter
        global lock
        lock.acquire()
        counter = counter + 1
        lock.release()
        mydb = mysql.connector.connect(
                host="34.34.73.69",
                user="root",
                password='1234'
        )
        mycursor = mydb.cursor()
        mydb.database = "nonduplicatesongsdatabase"
        song_id = request.id
        song_query = "SELECT * FROM Songs WHERE song_id = %s"
        mycursor.execute(song_query, (song_id,))
        song_result = mycursor.fetchone()

        if song_result is None:
            return GetSongDetailsResponse()

        song_id, title, artists, url, numtimesincharts, numcountrydif = song_result

        comment_query = "SELECT * FROM Comments WHERE song_id = %s"
        mycursor.execute(comment_query, (song_id,))
        comment_results = mycursor.fetchall()

        comments = []
        for comment_result in comment_results:
            comment_id, user_id, song_id, comment_text = comment_result
            comments.append(Comment(comment_id=comment_id, user_id=user_id, song_id=song_id, comment=comment_text))

        song = SongDetail(song_id=song_id, title=title, artists=artists, url=url, numtimesincharts=numtimesincharts, numcountrydif=numcountrydif, comments=comments)
        mydb.commit()
        mydb.close()
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
