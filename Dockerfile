FROM python:3.11.4
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat-traditional postgresql-client

RUN pip install poetry
WORKDIR /app

COPY pyproject.toml poetry.lock Makefile /app/
RUN make install-deploy

COPY . /app/

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
