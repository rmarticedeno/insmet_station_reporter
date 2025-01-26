FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache gcc libc-dev unixodbc-dev build-base

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x main.py

ENTRYPOINT while true; do sleep 15; done;