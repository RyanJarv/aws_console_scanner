FROM alpine:3 as base

ENV \
    # prevents python creating .pyc files \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apk add python3 py3-pip
RUN ln -s /usr/bin/python3 /usr/bin/python

# mitm-proxy dependencies
RUN apk add gcc python3-dev musl-dev libffi-dev openssl openssl-dev g++

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /opt/project
COPY ./ ./

ENTRYPOINT "/usr/bin/python -m aws_console_scanner"
