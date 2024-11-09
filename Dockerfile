FROM python:3.11-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt /app/
RUN python3 -m pip install --trusted-host https://mirror-pypi.runflare.com -i https://mirror-pypi.runflare.com/simple/ --upgrade pip
RUN pip install --trusted-host https://mirror-pypi.runflare.com -i https://mirror-pypi.runflare.com/simple/ -r requirements.txt
COPY ./core /app/

# RUN apt-get update \
# 	&& apt-get install -y --no-install-recommends \
# 		postgresql-client \
# 	&& rm -rf /var/lib/apt/lists/*

# Install gettext and compile translations
RUN apt-get update \
    && apt-get install -y gettext \
    && python manage.py compilemessages \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY ./core /app/