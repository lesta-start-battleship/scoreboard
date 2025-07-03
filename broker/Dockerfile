FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY /app/schemas ./app/schemas

COPY broker /app/broker

ENV PYTHONPATH=/app

LABEL authors="churakovra"
