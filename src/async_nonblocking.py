"""A simple, blocking/synchronous service."""

import aiohttp
import asyncio
import json
import os
import random
import urllib.request
from collections import Counter
from io import BytesIO

import asyncpg
from quart import Quart, request, send_file

app = Quart("async")

RESULTS = Counter()

POOL = None

async def count_filename(filename, latency):
    if latency is not None:
        await asyncio.sleep(int(latency))
    RESULTS[filename] += 1


async def get_dog_name(filename, latency):
    """Get the dog name(s)."""
    if latency is not None:
        await asyncio.sleep(int(latency))
    async with POOL.acquire() as conn:
        return (await conn.fetchrow("SELECT dog_names FROM photo WHERE filename LIKE $1", filename))[0]


@app.route("/")
async def get_dog():
    global POOL
    if POOL is None:
        POOL = await asyncpg.create_pool(os.environ.get("DB_URI"), min_size=1, max_size=10)
    latency = request.args.get("latency")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://canine/any?latency={latency or 0}") as resp:
            filename = resp.headers["X-Filename"]
            dog_name, _ = await asyncio.gather(get_dog_name(filename, latency), count_filename(filename, latency))
            return await send_file(BytesIO(await resp.read()), attachment_filename=dog_name, mimetype="image/jpeg")


@app.route("/stats")
async def get_stats():
    return json.dumps(RESULTS, indent=4, sort_keys=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
