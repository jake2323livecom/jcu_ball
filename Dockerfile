# syntax=docker/dockerfile:1
FROM python:3.9.6-alpine

# WORKDIR /code
# COPY . .
COPY requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /home/app
RUN addgroup -S app && adduser -S app -G app
ENV HOME=/home/app
ENV APP_HOME=/home/app/code/
RUN mkdir $APP_HOME
WORKDIR $APP_HOME
COPY . . 
RUN chmod -R 777 .
RUN chown -R app:app $APP_HOME
RUN apk update && apk add nano
USER app







