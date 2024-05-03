FROM python:3.11
ENV PYTHONUNBUFFERED 1
RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
# Instalar Gunicorn
RUN pip install gunicorn
COPY . /app/

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev libpq5 gdal-bin
RUN python -m pip install psycopg2
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]