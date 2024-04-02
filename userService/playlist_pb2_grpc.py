# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import playlist_pb2 as playlist__pb2


class PlayListServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Add = channel.unary_unary(
                '/PlayListService/Add',
                request_serializer=playlist__pb2.ModifyPlayListRequest.SerializeToString,
                response_deserializer=playlist__pb2.PlayListResponse.FromString,
                )
        self.Remove = channel.unary_unary(
                '/PlayListService/Remove',
                request_serializer=playlist__pb2.ModifyPlayListRequest.SerializeToString,
                response_deserializer=playlist__pb2.PlayListResponse.FromString,
                )
        self.Get = channel.unary_unary(
                '/PlayListService/Get',
                request_serializer=playlist__pb2.GetPlayListRequest.SerializeToString,
                response_deserializer=playlist__pb2.GetPlayListResponse.FromString,
                )


class PlayListServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Add(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Remove(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PlayListServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Add': grpc.unary_unary_rpc_method_handler(
                    servicer.Add,
                    request_deserializer=playlist__pb2.ModifyPlayListRequest.FromString,
                    response_serializer=playlist__pb2.PlayListResponse.SerializeToString,
            ),
            'Remove': grpc.unary_unary_rpc_method_handler(
                    servicer.Remove,
                    request_deserializer=playlist__pb2.ModifyPlayListRequest.FromString,
                    response_serializer=playlist__pb2.PlayListResponse.SerializeToString,
            ),
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=playlist__pb2.GetPlayListRequest.FromString,
                    response_serializer=playlist__pb2.GetPlayListResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'PlayListService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PlayListService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Add(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PlayListService/Add',
            playlist__pb2.ModifyPlayListRequest.SerializeToString,
            playlist__pb2.PlayListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Remove(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PlayListService/Remove',
            playlist__pb2.ModifyPlayListRequest.SerializeToString,
            playlist__pb2.PlayListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/PlayListService/Get',
            playlist__pb2.GetPlayListRequest.SerializeToString,
            playlist__pb2.GetPlayListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
