FROM python:3.8-slim

RUN apt-get update && apt-get install -y build-essential
RUN pip install fastapi
RUN pip install asyncpgsa aiohttp
RUN pip install quart hypercorn[uvloop]
RUN pip install flask uwsgi psycopg2-binary

RUN mkdir -p /usr/src/app /usr/src/dogs

EXPOSE 5000
EXPOSE 80

WORKDIR /usr/src/app
CMD ["echo", "noop"]

