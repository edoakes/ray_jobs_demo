import time
import sys

SMOKE_TEST = False
if len(sys.argv) > 1:
    print("Running smoke test")
    SMOKE_TEST = True

import ray

print("Initializing Ray...")
ray.init()

print("Doing feature preprocessing.")
ds = ray.data.range(10 if SMOKE_TEST else 100000000)
ds = ds.map(lambda x: x * 2)

print("Succeeded.")
