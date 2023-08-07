FROM python:3.11-slim

COPY ./requirements.txt /web/

WORKDIR /web

RUN pip install -r requirements.txt

COPY . /web
