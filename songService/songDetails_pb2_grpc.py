# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import songDetails_pb2 as songDetails__pb2


class SongDetailsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetSongDetails = channel.unary_unary(
                '/SongDetails/GetSongDetails',
                request_serializer=songDetails__pb2.GetSongDetailsRequest.SerializeToString,
                response_deserializer=songDetails__pb2.GetSongDetailsResponse.FromString,
                )


class SongDetailsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetSongDetails(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SongDetailsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetSongDetails': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSongDetails,
                    request_deserializer=songDetails__pb2.GetSongDetailsRequest.FromString,
                    response_serializer=songDetails__pb2.GetSongDetailsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'SongDetails', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SongDetails(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetSongDetails(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SongDetails/GetSongDetails',
            songDetails__pb2.GetSongDetailsRequest.SerializeToString,
            songDetails__pb2.GetSongDetailsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)