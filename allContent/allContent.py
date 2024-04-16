from concurrent import futures
import datetime
import random

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
import topCharts_pb2
import topCharts_pb2_grpc
import mysql.connector
import socket
from google.cloud.sql.connector import Connector
import pymysql
import sqlalchemy

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

        def init_connection_pool(connector: Connector) -> sqlalchemy.engine.Engine:
            def getconn() -> pymysql.connections.Connection:
                conn = connector.connect(
                    "spotifychartsgroup01:europe-west4:spotifychartsgroup01database",
                    "pymysql",
                    user="root",
                    password="1234",
                    db="allcontentdatabase"
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
                result = db_conn.execute(sqlalchemy.text("SELECT * from Songs LIMIT 10")).fetchall()
                songs = []
                for row in result:
                    print(row)
                    song = topCharts_pb2.Song(
                        id=row[0],
                        title=row[1],
                        rank=row[2],
                        artists=row[3],
                        chart=row[4]
                    )
                    print(song)
                    songs.append(song)
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
