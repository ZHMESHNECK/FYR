FROM python:3.9-alpine

WORKDIR /app/bot

# Встановлення залежностей
RUN apk --no-cache add musl-dev libffi-dev tzdata postgresql-dev make \
# Встанвлення  Firefox та geckodriver
&& apk --no-cache add firefox-esr \
&& wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz \
&& tar -zxf geckodriver-v0.33.0-linux64.tar.gz -C /usr/local/bin \
&& rm geckodriver-v0.33.0-linux64.tar.gz

# Встановлення бібліотек python
COPY requirements.txt requirements.txt
RUN apk --no-cache --virtual .build-deps add bzip2 libxslt-dev libx11-dev libxtst-dev wget \
&& pip3 install --upgrade setuptools \
&& pip3 install -r requirements.txt \
&& apk del .build-deps \
&& rm -rf /var/cache/apk/* \
# Створення дерикторій для Firefox
&& mkdir -p /opt/firefox \
&& ln -s /usr/bin/firefox-esr /opt/firefox/firefox

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
