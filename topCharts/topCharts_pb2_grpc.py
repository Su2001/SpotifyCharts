# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import topCharts_pb2 as topCharts__pb2


class TopChartsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetTopCharts = channel.unary_unary(
                '/TopCharts/GetTopCharts',
                request_serializer=topCharts__pb2.GetTopChartsRequest.SerializeToString,
                response_deserializer=topCharts__pb2.GetTopChartsResponse.FromString,
                )


class TopChartsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetTopCharts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TopChartsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetTopCharts': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTopCharts,
                    request_deserializer=topCharts__pb2.GetTopChartsRequest.FromString,
                    response_serializer=topCharts__pb2.GetTopChartsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'TopCharts', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TopCharts(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetTopCharts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/TopCharts/GetTopCharts',
            topCharts__pb2.GetTopChartsRequest.SerializeToString,
            topCharts__pb2.GetTopChartsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)