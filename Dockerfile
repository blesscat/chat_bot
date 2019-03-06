FROM python:3.7
MAINTAINER Bless

COPY . /usr/bin/telegramBot
WORKDIR /usr/bin/telegramBot

RUN pip install -r requirements.txt

CMD gunicorn -w 4 -b 0.0.0.0:5000 run:app
