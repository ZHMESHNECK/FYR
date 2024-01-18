FROM python:3.9-alpine
WORKDIR /app

RUN apk --no-cache add musl-dev make libgcc libstdc++ libx11 libxext libintl libxslt tzdata postgresql-dev  \
&& apk add --no-cache --virtual .build-deps bzip2 freetype-dev libffi-dev libxslt-dev libx11-dev libxtst-dev tzdata wget \
&& wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz \
&& tar -zxf geckodriver-v0.33.0-linux64.tar.gz -C /usr/local/bin \
&& rm geckodriver-v0.33.0-linux64.tar.gz \
&& wget -O firefox.tar.bz2 "https://download.mozilla.org/?product=firefox-latest&os=linux64" \
&& tar xjf firefox.tar.bz2 -C /opt/ \
&& ln -s /opt/firefox/firefox /usr/bin/firefox \
&& rm firefox.tar.bz2 \
&& apk del .build-deps \
&& rm -rf /var/cache/apk/*

WORKDIR /app/bot

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade setuptools \
&& pip3 install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .