FROM alpine:3 as base

ENV \
    # prevents python creating .pyc files \
    #PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    #PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    \
    # poetry \
    # https://python-poetry.org/docs/configuration/#using-environment-variables \
    # make poetry install to this location \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    \
    # paths \
    # this is where our requirements + virtual environment will live \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
RUN echo "export PATH='$PATH:/$POETRY_HOME/.poetry/bin'" >> /etc/profile

RUN apk add python3 py3-pip
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN wget -O - https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# mitm-proxy dependencies
RUN apk add gcc python3-dev musl-dev libffi-dev openssl openssl-dev g++

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry install

WORKDIR /opt/project
COPY ./ ./
