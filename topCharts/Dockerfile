FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY topCharts/ /service/topCharts/

WORKDIR /service/topCharts
RUN pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/topCharts.proto

# EXPOSE 5000
ENV FLASK_APP=topCharts.py
# ENTRYPOINT [ "flask", "run", "--host=0.0.0.0"]