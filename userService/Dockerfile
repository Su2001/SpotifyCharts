FROM python

RUN mkdir /service
COPY ../protobufs/ /service/protobufs/
COPY ../userService/ /service/userService/

WORKDIR /service/userService

RUN pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/playlist.proto
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/health.proto

EXPOSE 50051
ENTRYPOINT [ "python","-u", "UserService.py" ]