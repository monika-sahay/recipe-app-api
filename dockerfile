FROM python:3.7-alpine
MAINTAINER monikasahay
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY ./app/ /app
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps
RUN adduser -D user
RUN chown -R user:user app/
USER user
