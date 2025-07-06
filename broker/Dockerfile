FROM python:3.12-slim

WORKDIR /app
COPY broker/requirements.txt .

RUN pip install -r requirements.txt

COPY shared ./shared

COPY broker ./broker

ENV PYTHONPATH=/app

LABEL authors="churakovra"
