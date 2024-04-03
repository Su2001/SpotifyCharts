FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY allContent/ /service/allContent/

WORKDIR /service/allContent
RUN pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/topCharts.proto

EXPOSE 50051
ENTRYPOINT [ "python", "allContent.py" ]