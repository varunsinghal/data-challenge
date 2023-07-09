FROM python:3.8-slim-buster

RUN apt-get update

COPY requirements.txt .

RUN pip install poetry
RUN poetry install 
