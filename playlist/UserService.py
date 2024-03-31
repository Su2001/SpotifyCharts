from concurrent import futures
import random

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from playlist_pb2 import(
    AddPlayListRequest,
    AddPlayListResponse,
    GetPlayListRequest,
    GetPlayListResponse,
    RemovePlayListRequest,
    RemovePlayListResponse
)

import playlist_pb2_grpc

temp_dic = {1:[1],2:[2]}

class AddPlayListService(playlist_pb2_grpc.AddPlayListServicer):
    def Add(self, request, context):
        #interacte bd
        if request.user_id not in temp_dic:
            raise NotFound("Category not found")
        else :
            temp_dic[request.user_id].append(request.song_id)
        print(temp_dic)
        return AddPlayListResponse(response=1)

class RemovePlayListService(playlist_pb2_grpc.RemovePlayListServicer):
    def Remove(self, request, context):
        #interacte bd
        if request.user_id not in temp_dic:
            raise NotFound("Category not found")
        else :
            temp_dic[request.user_id].remove(request.song_id)
        print("remove ")
        return RemovePlayListResponse(response=1)

class GetPlayListService(playlist_pb2_grpc.GetPlayListServicer):
    def Get(self, request, context):
        #interacte bd
        if request.user_id not in temp_dic:
            raise NotFound("Category not found")
        print("get")
        return GetPlayListResponse(songs=temp_dic[request.user_id])

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    playlist_pb2_grpc.add_RemovePlayListServicer_to_server(
        RemovePlayListService(), server
    )
    playlist_pb2_grpc.add_AddPlayListServicer_to_server(
        AddPlayListService(), server
    )

    playlist_pb2_grpc.add_GetPlayListServicer_to_server(
        GetPlayListService(), server
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