FROM python:3.11.9-slim-bullseye

ENV COMMAND='--help'

WORKDIR /engine-romy

COPY . /engine-romy

EXPOSE 1-65535

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install .

CMD ["/bin/bash", "-c", "engine_romy ${COMMAND}"]
