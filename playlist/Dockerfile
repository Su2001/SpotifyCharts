FROM python

RUN mkdir /service
COPY ../protobufs/ /service/protobufs/
COPY ../playlist/ /service/playlistService/

WORKDIR /service/playlistService

RUN pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/playlist.proto

EXPOSE 8080
ENV FLASK_APP=PlayListService.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=8080"]