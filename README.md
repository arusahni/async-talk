# Async All The Way Down resources

# Viewing the slides

Open `Async All The Way Down.pdf` in your PDF viewer of choice.

# Running the code

1. Bring up the docker environment: `docker-compose up`
2. Visit the services:
   * Canine Microservice: http://localhost:8000
   * Sync webapp: http://localhost:5000
   * Async blocking webapp: http://localhost:5010
   * Async nonblocking webapp: http://localhost:5020
3. Add a `latency` parameter with the number of seconds in order to simulate the appropriate amount of delay.
   * e.g., `http://localhost:5010/?latency=10` to simulate 10 seconds of delay on every async operation.

# Benchmarking the code

1. Install [drill](https://github.com/fcsonline/drill)
2. Run each benchmark:
   * `drill --benchmark benchmarks/sync.yml --stats`
   * `drill --benchmark benchmarks/async_blocking.yml --stats`
   * `drill --benchmark benchmarks/async_nonblocking.yml --stats`

# Dogs

Please support an animal rescue or shelter near you! Motley came from [Wolf Trap Animal Rescue](https://wolftrapanimalrescue.com/).


# License

All dog images (contents of the `dogs/` folder, slides with photos of dogs) are
not licensed for redistribution, publication, commercial use, personal use
(outside of running the presentation locally), or broadcast. Aru Sahni retains
all rights to them.

All code and presentation text are available under the GPLv3 license, unless
otherwise specified.
