FROM python:3.11-slim

COPY ./ /src/

WORKDIR /src

RUN pip install -r requiruments.txt

ENTRYPOINT python run_bot.py