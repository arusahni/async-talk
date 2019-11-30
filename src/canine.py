"""The canine service."""
import asyncio
import random
from glob import glob
from datetime import timedelta

from quart import Quart, make_response, request, send_file

DIRECTORY = "../dogs/"

app = Quart("canine")
app.config["SEND_FILE_MAX_AGE"] = timedelta(microseconds=1)


@app.route("/dog")
async def get_dog():
    """Get a photo of one dog."""
    latency = request.args.get("latency")
    if latency:
        await asyncio.sleep(int(latency))
    files = glob(f"{DIRECTORY}single/*.jpg")
    filename = random.choice(files)
    return await make_response(await send_file(filename), {"X-Filename": filename.split("/")[-1]})


@app.route("/dogs")
async def get_dogs():
    """Get a photo of multiple dogs."""
    latency = request.args.get("latency")
    if latency:
        await asyncio.sleep(int(latency))
    files = glob(f"{DIRECTORY}group/*.jpg")
    filename = random.choice(files)
    return await make_response(await send_file(filename), {"X-Filename": filename.split("/")[-1]})


@app.route("/any")
async def get_any():
    """Get a photo of one or many dogs."""
    latency = request.args.get("latency")
    if latency:
        await asyncio.sleep(int(latency))
    files = glob(f"{DIRECTORY}/**/*.jpg")
    filename = random.choice(files)
    return await make_response(await send_file(filename), {"X-Filename": filename.split("/")[-1]})


@app.route("/")
async def index():
    """The index."""
    return '<a href="/dog">One dog</a><br /><a href="/dogs">More dogs</a><a href="/any">Any dog</a>'


if __name__ == "__main__":
    app.run(port=8000)
