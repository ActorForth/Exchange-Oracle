FROM python:3.7

WORKDIR /app

RUN apt-get update && apt-get install -y python-pip python3.7 python3-setuptools autoconf libtool pkg-config python3-dev build-essential

COPY ./requirements.txt /app/requirements.txt

COPY . /app

# ENV AUCTION_DEBUG_MODE False
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 2222

WORKDIR /app

RUN pip install -r requirements.txt