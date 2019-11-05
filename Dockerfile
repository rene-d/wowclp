FROM alpine

RUN apk update \
&&  apk add --no-cache python3 vim file curl gcc musl-dev python3-dev

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN pip3 install -U pip click requests black

WORKDIR /host
