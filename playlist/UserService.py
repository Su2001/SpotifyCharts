from concurrent import futures
import random

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from playlist_pb2 import(
    ModifyPlayListRequest,
    GetPlayListRequest,
    GetPlayListResponse,
    PlayListResponse
)

import playlist_pb2_grpc

temp_dic = {1:[1],2:[2]}

class PlayListService(playlist_pb2_grpc.PlayListServiceServicer):
    def Add(self, request, context):
        #interacte bd
        if request.user_id not in temp_dic:
            return PlayListResponse(response=-1)
        else :
            temp_dic[request.user_id].append(request.song_id)
        print(temp_dic)
        return PlayListResponse(response=1)

    def Remove(self, request, context):
        #interacte bd
        if request.user_id not in temp_dic:
            return PlayListResponse(response=-1)
        else :
            temp_dic[request.user_id].remove(request.song_id)
        print("remove ")
        return PlayListResponse(response=1)

    def Get(self, request, context):
        #interacte bd
        if request.user_id not in temp_dic:
            return GetPlayListResponse(response = -1,songs=[]) 
        print("get")
        return GetPlayListResponse(response = 1,songs=temp_dic[request.user_id])    

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    playlist_pb2_grpc.add_PlayListServiceServicer_to_server(
        PlayListService(), server
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