"""A simple, blocking/synchronous service."""

import json
import os
import random
import time
import urllib.request
from collections import Counter

import psycopg2
import psycopg2.pool
from flask import Flask, request, send_file

app = Flask("sync")

RESULTS = Counter()

POOL = psycopg2.pool.SimpleConnectionPool(1, 10, dsn=os.environ.get("DB_URI"))

def count_filename(filename, latency):
    if latency:
        time.sleep(int(latency))
    RESULTS[filename] += 1


def setup_db():
    conn = POOL.getconn()
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS photo (
                        filename varchar PRIMARY KEY,
                        dog_names varchar NOT NULL
                    );
                    INSERT INTO photo (filename, dog_names) VALUES
                        ('00002IMG_00002_BURST20190203152303_COVER.jpg', 'Motley, Penny'),
                        ('IMG_20190210_152221.jpg', 'Motley, Copper'),
                        ('IMG_20190316_130222.jpg', 'Motley, Magnus'),
                        ('IMG_20190824_162821.jpg', 'Motley, Molly'),
                        ('IMG_20191006_141954.jpg', 'Motley, Kali'),
                        ('00100dPORTRAIT_00100_BURST20190519170426160_COVER~2.jpg', 'Motley'),
                        ('00100dPORTRAIT_00100_BURST20190914210439554_COVER.jpg', 'Motley'),
                        ('IMG_20190314_191827.jpg', 'Motley'),
                        ('IMG_20190324_102748.jpg', 'Motley'),
                        ('IMG_20190331_172815.jpg', 'Motley'),
                        ('IMG_20190406_155234.jpg', 'Motley'),
                        ('IMG_20190511_081500.jpg', 'Motley')
                    ON CONFLICT DO NOTHING;
                """
                )
    finally:
        conn.close()
        POOL.putconn(conn)


def get_dog_name(filename, latency):
    """Get the dog name(s)."""
    conn = POOL.getconn()
    if latency is not None:
        time.sleep(int(latency))
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT dog_names FROM photo WHERE filename LIKE %s", (filename,))
                value = cursor.fetchone()
                return value[0]
    finally:
        conn.close()


@app.route("/")
def get_dog():
    latency = request.args.get("latency")
    image = urllib.request.urlopen(f"http://canine/any?latency={latency or 0}")
    filename = image.info()["X-Filename"]
    count_filename(filename, latency)
    dog_name = get_dog_name(filename, latency)
    return send_file(image, attachment_filename=dog_name, mimetype="image/jpeg")


@app.route("/stats")
def get_stats():
    return json.dumps(RESULTS, indent=4, sort_keys=True)


if __name__ == "__main__":
    setup_db()
    app.run(host="0.0.0.0", port=5000)
