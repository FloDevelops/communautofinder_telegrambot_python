FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y \
   pkg-config \
   gcc \
   default-libmysqlclient-dev \
   && rm -rf /var/lib/apt/lists/*

COPY . /code
RUN pip install poetry && poetry config virtualenvs.create false && poetry install

CMD ["poetry", "run", "start"]