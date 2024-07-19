FROM python:3.11.9-slim-bullseye

ENV COMMAND='--help'

WORKDIR /engine-romy

COPY . /engine-romy

EXPOSE 1-65535

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata

RUN ln -fs /usr/share/zoneinfo/Asia/Jakarta /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install .