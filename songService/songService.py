from concurrent import futures

from flask import Flask, render_template
import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
import search_pb2
import search_pb2_grpc
import songComments_pb2_grpc

from songComments_pb2 import {
    AddCommentRequest,
    AddCommentResponse,
    UpdateCommentRequest,
    UpdateCommentResponse,
    RemoveCommentRequest,
    RemoveCommentResponse
}

app = Flask(__name__)

class Search(search_pb2_grpc.SearchServicer):
    def GetSearch(self, request, context):
        print("ENTROU NO SONG")
        #FALTA FAZER O PEDIDO à BD PARA OBTER O TOP CHARTS
        # gotTopCharts = 1
        # return topCharts_pb2.GetTopChartsResponse(topcharts = gotTopCharts)
        return search_pb2.GetSearchResponse(songs = [
            search_pb2.Song(id= 1,title = 'TESTE',artists = 'ARTISTA'), search_pb2.Song(id= 2,title = 'AAAAAAAAAA',artists = 'ARTISTA2')
        ])

class CommentService(songComments_pb2_grpc.AddCommentServicer, songComments_pb2_grpc.UpdateCommentServicer, songComments_pb2_grpc.RemoveCommentServicer):
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
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
