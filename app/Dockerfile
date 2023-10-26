FROM python:3.11-slim

RUN apt update; apt-get install -y libglib2.0-0

COPY ./ /src/

WORKDIR /src

RUN pip install -r requiruments.txt

ENTRYPOINT python run_bot.py