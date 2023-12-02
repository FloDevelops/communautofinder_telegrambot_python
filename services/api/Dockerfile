FROM python:3.10-slim

WORKDIR /code

COPY . /code
RUN pip install poetry && poetry config virtualenvs.create false && poetry install

CMD ["poetry", "run", "dev"]