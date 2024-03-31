from concurrent import futures
import random

from flask import Flask, render_template
import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
import topCharts_pb2
import topCharts_pb2_grpc

app = Flask(__name__)

class TopCharts(topCharts_pb2_grpc.TopChartsServicer):
    def GetTopCharts(self, request, context):
        print("ENTROU NO ALLCONTENT")
        #FALTA FAZER O PEDIDO à BD PARA OBTER O TOP CHARTS
        # return topCharts_pb2.GetTopChartsResponse(topcharts = gotTopCharts)
        return topCharts_pb2.GetTopChartsResponse(songs = [
            topCharts_pb2.Song(id= 1,title = 'TESTE',artists = 'ARTISTA',rank = 4), topCharts_pb2.Song(id= 2,title = 'AAAAAAAAAA',artists = 'ARTISTA',rank = 4)
        ])

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    topCharts_pb2_grpc.add_TopChartsServicer_to_server(
        TopCharts(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
