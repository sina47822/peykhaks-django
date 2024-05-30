FROM python:3.11.4-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./core /app/

# RUN apt-get update \
# 	&& apt-get install -y --no-install-recommends \
# 		postgresql-client \
# 	&& rm -rf /var/lib/apt/lists/*

