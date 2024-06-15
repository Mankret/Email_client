FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        libpq-dev \
        gcc \
        python3-dev \
        musl-dev \
        netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY  ./requirements.txt .

RUN pip install -r requirements.txt

COPY . /app
COPY ./docker/entrypoint.sh ./docker/runserver.sh
RUN chmod +x /app/docker/entrypoint.sh /app/docker/runserver.sh

ENTRYPOINT ["/app/docker/entrypoint.sh"]
