FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY allContent/ /service/allContent/

WORKDIR /service/allContent
RUN pip install -r requirements.txt
RUN pip install "cloud-sql-python-connector[pymysql]"
RUN pip install sqlalchemy

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/topCharts.proto
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/health.proto

EXPOSE 50051
ENTRYPOINT [ "python","-u", "allContent.py" ]