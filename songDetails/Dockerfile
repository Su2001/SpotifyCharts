FROM python

RUN mkdir /service
COPY ../protobufs/ /service/protobufs/
COPY ../songDetails/ /service/songDetails/

WORKDIR /service/songDetails
RUN pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/songDetails.proto

EXPOSE 5003
ENV FLASK_APP=songDetailsService.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=5003"]