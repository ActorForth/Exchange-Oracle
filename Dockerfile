FROM python:3.7.11-slim

WORKDIR /app

RUN apt-get update && apt-get install

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./src/exchange.py /app/exchange.py

#COPY . /app

# ENV AUCTION_DEBUG_MODE False
# ENV FLASK_RUN_HOST=0.0.0.0

#EXPOSE 2222

CMD ["gunicorn", "--bind 0.0.0.0:2222", "--timeout=600", "exchange:app", "-w 1", "--threads 5"]
