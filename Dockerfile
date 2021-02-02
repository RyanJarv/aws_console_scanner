FROM alpine:3 as base

RUN apk add python3 py3-pip
RUN ln -s /usr/bin/python3 /usr/bin/python

# mitm-proxy dependencies
RUN apk add gcc python3-dev musl-dev libffi-dev openssl openssl-dev g++

WORKDIR /opt/project
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./ ./

RUN pip install .

ENTRYPOINT ["python", "-m", "aws_console_scanner"]
