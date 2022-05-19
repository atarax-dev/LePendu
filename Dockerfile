# pull official base image
FROM python:3.10-alpine

# set work directory
WORKDIR /app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# run gunicorn
CMD gunicorn LePendu.wsgi:application --bind 0.0.0.0:$PORT
