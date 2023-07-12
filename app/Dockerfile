FROM python:3.11-slim

COPY ./ /src/

WORKDIR /src

RUN pip install -r requiruments.txt

ENTRYPOINT sleep 15; python run_bot.py