FROM python:3

COPY . /code
WORKDIR /code

RUN python ./setup.py install
RUN mkdir /output
RUN mkdir /input
RUN mkdir /config
