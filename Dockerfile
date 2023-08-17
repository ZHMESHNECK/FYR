FROM python:3.9
WORKDIR /app

RUN echo "===> Installing geckodriver and firefox..." && \
wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz && \
tar -zxf geckodriver-v0.33.0-linux64.tar.gz -C /usr/local/bin && \
chmod +x /usr/local/bin/geckodriver && \
rm geckodriver-v0.33.0-linux64.tar.gz && \
\
apt-get update && apt-get -y install libgtk-3-0 libasound2 bzip2 libxtst6 libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev && \
FIREFOX_SETUP=firefox-setup.tar.bz2 && \
apt-get purge firefox && \
wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
tar xjf $FIREFOX_SETUP -C /opt/ && \
ln -s /opt/firefox/firefox /usr/bin/firefox && \
rm $FIREFOX_SETUP
WORKDIR /app/bot
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setuptools \
&& pip3 install -r requirements.txt
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . .