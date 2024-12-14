FROM python:3.11-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update
# نصب بسته‌های لازم
RUN apt-get install -y \
    libglib2.0-0 \
    libglib2.0-dev \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    && apt-get clean

# نصب وابستگی‌های Python
COPY requirements.txt /app/
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./core /app/

# RUN apt-get update \
# 	&& apt-get install -y --no-install-recommends \
# 		postgresql-client \
# 	&& rm -rf /var/lib/apt/lists/*

# Install gettext and compile translations
# RUN apt-get update \
#     && apt-get install -y gettext \
#     && python manage.py compilemessages \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*
# COPY ./core /app/