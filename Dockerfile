FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache gcc libc-dev unixodbc-dev

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY install_driver.sh .

COPY . .

RUN chmod +x main.py

ENTRYPOINT while true; do sleep 15