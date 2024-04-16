FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY songService/ /service/songService/

WORKDIR /service/songService

RUN pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/search.proto
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/songComments.proto
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/songDetails.proto
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/health.proto

EXPOSE 50051
ENTRYPOINT [ "python", "-u", "songService.py" ]