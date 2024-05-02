FROM python:3.11
ENV PYTHONUNBUFFERED 1
RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
COPY . /app/

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev libpq5 gdal-bin
RUN python -m pip install psycopg2
