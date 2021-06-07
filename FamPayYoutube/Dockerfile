FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN apk update && apk add alpine-sdk gcc musl-dev python3-dev libffi-dev openssl-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080
