FROM python:3.10-slim-buster
RUN apt-get update \
    && apt-get install -y --no-install-recommends apt-utils \
    && apt-get install -y --no-install-recommends curl

WORKDIR /api
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

RUN python -m manage makemigrations user
RUN python -m manage makemigrations search
RUN python -m manage migrate user
RUN python -m manage migrate search

CMD python -m manage runserver 0.0.0.0:8000