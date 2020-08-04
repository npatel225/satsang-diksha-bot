FROM python:3-slim

RUN apt update && apt upgrade -y && apt install gcc build-essential libssl-dev libffi-dev python3-dev -y
COPY . /app
WORKDIR /app
ENV PYTHONPATH=/app
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

CMD python3 main.py