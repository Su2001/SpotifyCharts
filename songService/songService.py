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
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234"
)
mycursor = mydb.cursor()
mydb.database = "nonduplicatesongsdatabase"

app = Flask(__name__)

class Search(search_pb2_grpc.SearchServicer):
    def GetSearch(self, request, context):
        query = "SELECT song_id, title, artist FROM nonduplicatesongsdatabase.songs WHERE title LIKE %s"
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
        return search_pb2.GetSearchResponse(songs=songs)

class CommentService(songComments_pb2_grpc.CommentServiceServicer):
    def Add(self, request, context):

        query = "INSERT INTO nonduplicatesongsdatabase.comments (user_id, song_id, comment) VALUES (%d, %d, %s);"
        mycursor.execute(query, (request.user_id, request.song_id, request.comment,))
        print("Inserted comment: ", request.user_id, request.song_id, request.comment)
        return AddCommentResponse(response=1)

    def Update(self, request, context):
        query = "UPDATE nonduplicatesongsdatabase.comments SET comment = %s WHERE user_id = %d AND song_id = %d AND comment_id =%d;"
        mycursor.execute(query, (request.comment, request.user_id, request.song_id,))
        print("Updated comment. The new comment is: ", request.comment)
        return UpdateCommentResponse(response=1)

    def Remove(self, request, context):
        query = "DELETE FROM nonduplicatesongsdatabase.comments WHERE user_id = %d AND song_id = %d AND comment_id = %d;"
        mycursor.execute(query, (request.user_id, request.song_id,))
        print("Removed comment for user", request.user_id, "and song", request.song_id)
        return RemoveCommentResponse(response=1)

class SongDetails(songDetails_pb2_grpc.SongDetailsServicer):
    def GetSongDetails(self, request, context):
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
        return songDetails_pb2.GetSongDetailsResponse(song=song)


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
