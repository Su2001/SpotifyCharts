from concurrent import futures

from flask import Flask, render_template
import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
import search_pb2
import search_pb2_grpc
import songComments_pb2_grpc

from songComments_pb2 import (
    AddCommentRequest,
    AddCommentResponse,
    UpdateCommentRequest,
    UpdateCommentResponse,
    RemoveCommentRequest,
    RemoveCommentResponse
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
        #interacte bd
        # if request.user_id not in temp_dic:
        #     raise NotFound("Category not found")
        # else :
        #     temp_dic[request.user_id].append(request.song_id)
        # print(temp_dic)
        return AddCommentResponse(response=1)

    def Update(self, request, context):
        #interacte bd
        # if request.user_id not in temp_dic:
        #     raise NotFound("Category not found")
        # else :
        #     temp_dic[request.user_id].remove(request.song_id)
        # print("remove ")
        return UpdateCommentResponse(response=1)

    def Remove(self, request, context):
        #interacte bd
        # if request.user_id not in temp_dic:
        #     raise NotFound("Category not found")
        # else :
        #     temp_dic[request.user_id].remove(request.song_id)
        # print("remove ")
        return RemoveCommentResponse(response=1)

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
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
