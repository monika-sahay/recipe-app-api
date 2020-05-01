FROM python:3.7-alpine
MAINTAINER monikasahay
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt requirements.txt
RUN pip install -r /requirements.txt
RUN mkdir /app
WORKDIR /app
COPY ./app/ /app
RUN chown -R $user:$user app/
RUN adduser -D user
USER user
