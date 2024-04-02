FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY songComments/ /service/songComments/

WORKDIR /service/songComments

RUN pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/songComments.proto

EXPOSE 50051
ENTRYPOINT [ "python", "SongCommentsService.py" ]