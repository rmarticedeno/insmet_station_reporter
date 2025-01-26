FROM python:3.11-alpine

WORKDIR /app

COPY install_driver.sh .

run apk add curl gpg && ./install_driver.sh

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x main.py

ENTRYPOINT while true; do sleep 15; done;