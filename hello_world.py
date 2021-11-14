import ray
ray.init()

print("Hello from the driver!")
@ray.remote
def say_hi():
    print("HIHIHI")

ray.get([say_hi.remote() for _ in range(5)])
