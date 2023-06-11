FROM python:3.10-slim

WORKDIR /app

COPY server/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY server .