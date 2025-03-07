# stdlib
import os

# 3rd party
import redis

redis_conn = redis.StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"))
pubsub = redis_conn.pubsub(ignore_subscribe_messages=True)


def setup_webapp(*_):
    pubsub.run_in_thread(daemon=True, sleep_time=0.1)
