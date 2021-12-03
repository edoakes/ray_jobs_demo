import argparse
import logging

from fastapi import FastAPI

import ray
from ray import serve

serve.start(detached=True)

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("--max-count", type=int, required=False, default=10)

app = FastAPI()

@serve.deployment(route_prefix="/")
@serve.ingress(app)
class Counter:
    def __init__(self, max_count: int = 10):
        self._count = 0
        self._max_count = max_count
        logger.info(f"Starting with max_count: {max_count}")

    @app.get("/")
    def get(self):
        return f"Current count: {self._count}"

    @app.get("/reset")
    def reset(self):
        self._count = 0
        return f"Current count: {self._count}"

    @app.get("/increment")
    def increment(self):
        self._count += 1
        return f"Current count: {self._count}"

    @app.get("/healthz")
    def healthcheck(self):
        if self._count >= self._max_count:
            raise Exception("Count exceeded maximum.")

if __name__ == "__main__":
    args = parser.parse_args()
    Counter.deploy(max_count=args.max_count)
