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

# EXPOSE 5000
ENV FLASK_APP=songService.py
# ENTRYPOINT [ "flask", "run", "--host=0.0.0.0"]