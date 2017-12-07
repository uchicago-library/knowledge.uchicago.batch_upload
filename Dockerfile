FROM python:3

COPY . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN python ./setup.py install
RUN mkdir /output
RUN mkdir /input
RUN mkdir /config
