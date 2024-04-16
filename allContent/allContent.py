from concurrent import futures
import datetime
import random

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
import topCharts_pb2
import topCharts_pb2_grpc
import mysql.connector
import socket

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

class TopCharts(topCharts_pb2_grpc.TopChartsServicer):
    def GetTopCharts(self, request, context):
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
        mydb.database = "allcontentdatabase"
        query = "SELECT song_id, title, `rank`, artist, chart FROM allcontentdatabase.Songs WHERE date = %s AND region = %s"
        mycursor.execute(query, (request.date, request.country,))
        result = mycursor.fetchall()
        songs = []
        for row in result:
            song = topCharts_pb2.Song(
                id=row[0],
                title=row[1],
                rank=row[2],
                artists=row[3],
                chart=row[4]
            )
            songs.append(song)
            # print("Fetched song:", song)
        mydb.close()
        lock.acquire()
        counter = counter - 1
        lock.release()
        return topCharts_pb2.GetTopChartsResponse(songs=songs)


def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=MAX), interceptors=interceptors
    )
    topCharts_pb2_grpc.add_TopChartsServicer_to_server(
        TopCharts(), server
    )
    health_pb2_grpc.add_HealthServicer_to_server(
        HealthCheck(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
