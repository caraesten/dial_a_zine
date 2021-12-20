# syntax=docker/dockerfile:1

ARG ISSUE_DIR=newsession_issue2

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY dialazine dialazine
COPY $ISSUE_DIR $ISSUE_DIR

EXPOSE 23/tcp

CMD [ "python3", "dialazine/server.py" ]
