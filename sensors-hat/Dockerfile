FROM resin/raspberrypi3-debian:stretch

ENV INITSYSTEM on

RUN apt-get update && apt-get install -yq \
  python3 \
  python3-sense-hat \
  python3-pip \
  vim \
  wget && \
  apt-get clean && rm -rf /var/lib/apt/lists/* && \
  pip3 install paho-mqtt

COPY . /usr/src/app
WORKDIR /usr/src/app

CMD ["python3", "/usr/src/app/main.py"]