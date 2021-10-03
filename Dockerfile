FROM ubuntu

# Install pulse audio
RUN apt-get -qq update
RUN apt-get install -y tzdata
RUN apt-get install -y pulseaudio socat
RUN apt-get install -y alsa-utils

# Use custom entrypoint
COPY entrypoint.sh /opt/bin/entrypoint.sh

# COPY Script
COPY SpaceRecorder.py /opt/bin/SpaceRecorder.py
COPY settings.yaml /opt/bin/settings.yaml
COPY client_secret.json /opt/bin/client_secret.json
COPY credentials.json /opt/bin/credentials.json

# add root user to group for pulseaudio access
RUN adduser root pulse-access

# Install Python & Modules
RUN apt-get install -y python3 python3-pip

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN apt-get install -y wget
RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN apt-get update
RUN apt-get install -y google-chrome-stable
RUN apt-get install -y python3-selenium
RUN pip install selenium
RUN pip install chromedriver-binary
RUN pip install chromedriver-binary-auto
RUN pip install psutil
RUN pip install schedule
RUN pip install pydrive
RUN pip install requests
RUN pip install tweepy
RUN apt-get install -y sox
RUN apt-get install -y libsox-fmt-all

ENTRYPOINT /opt/bin/entrypoint.sh