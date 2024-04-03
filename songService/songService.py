from concurrent import futures

from flask import Flask, render_template
import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
import search_pb2
import search_pb2_grpc
import songComments_pb2_grpc
import songDetails_pb2_grpc


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


class Search(search_pb2_grpc.SearchServicer):
    def GetSearch(self, request, context):
        mydb = mysql.connector.connect(
            host="172.21.0.2",
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
        return search_pb2.GetSearchResponse(songs=songs)

class CommentService(songComments_pb2_grpc.CommentServiceServicer):
    def Add(self, request, context):
        mydb = mysql.connector.connect(
            host="172.21.0.2",
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
        return AddCommentResponse(response=1)

    def Update(self, request, context):
        mydb = mysql.connector.connect(
            host="172.21.0.2",
                user="root",
                password='1234'
        )
        mycursor = mydb.cursor()
        mydb.database = "nonduplicatesongsdatabase"
        query = "UPDATE nonduplicatesongsdatabase.Comments SET comment = %s WHERE user_id = %s AND song_id = %s AND comment_id =%s"
        mycursor.execute(query, (request.comment, request.user_id, request.song_id,))
        print("Updated comment. The new comment is: ", request.comment)
        mydb.commit()
        mydb.close()
        return UpdateCommentResponse(response=1)

    def Remove(self, request, context):
        mydb = mysql.connector.connect(
            host="172.21.0.2",
                user="root",
                password='1234'
        )
        mycursor = mydb.cursor()
        mydb.database = "nonduplicatesongsdatabase"
        query = "DELETE FROM nonduplicatesongsdatabase.Comments WHERE user_id = %s AND song_id = %s AND comment_id = %s"
        mycursor.execute(query, (request.user_id, request.song_id,))
        print("Removed comment for user", request.user_id, "and song", request.song_id)
        mydb.commit()
        mydb.close()
        return RemoveCommentResponse(response=1)

class SongDetails(songDetails_pb2_grpc.SongDetailsServicer):
    def GetSongDetails(self, request, context):
        mydb = mysql.connector.connect(
            host="172.21.0.2",
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
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
    
if __name__ == "__main__":
    serve()
