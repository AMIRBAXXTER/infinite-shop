FROM python:3.11

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/PY/BIN:$PATH"

COPY requirements.txt /code/
COPY . /code/

RUN pip install -U pip
RUN pip install -r requirements.txt
