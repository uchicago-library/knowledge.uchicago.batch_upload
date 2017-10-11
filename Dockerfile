FROM python:3

COPY . /code
WORKDIR /code

RUN python ./setup.py install
RUN mkdir /output
RUN ["chmod", "+x", "bin/saf-generation.py"]

CMD ["touch", "/output/foo.text"]

ENTRYPOINT ["python", "bin/saf-generation.py"]