FROM python

RUN mkdir /service
COPY ../protobufs/ /service/protobufs/
COPY ../search/ /service/search/

WORKDIR /service/search
RUN pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/search.proto

EXPOSE 5002
ENV FLASK_APP=searchService.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=5002"]