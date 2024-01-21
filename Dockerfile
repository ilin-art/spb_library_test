FROM python:3.10

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN pip install celery[redis]
RUN apt-get update && apt-get install -y redis-tools

ENV PATH="/usr/bin/redis-cli:${PATH}"
