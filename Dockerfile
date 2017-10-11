FROM python:3

COPY . /code
WORKDIR /code

RUN python ./setup.py install
RUN mkdir /output

ENTRYPOINT ["python", "bin/saf-generation.py"]