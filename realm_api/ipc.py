# stdlib
import asyncio as aio
import json
import os
from uuid import uuid4

# 3rd party
import redis

redis_conn = redis.StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"))
pubsub = redis_conn.pubsub(ignore_subscribe_messages=True)


async def ipc_op(op: str, *args, timeout=3, **kwargs):
    """Perform an IPC operation and await the response."""

    q = aio.Queue()

    def handler(message: dict):
        data = json.loads(message["data"])
        aio.new_event_loop().run_until_complete(q.put(data))

    uuid = str(uuid4())
    pubsub.subscribe(**{uuid: handler})

    try:
        redis_conn.publish(
            "ipc",
            json.dumps(
                {
                    "uuid": uuid,
                    "op": op,
                    "args": args,
                    "kwargs": kwargs,
                }
            ),
        )

        return await aio.wait_for(q.get(), timeout)

    finally:
        pubsub.unsubscribe(uuid)


def setup_webapp(*_):
    pubsub.run_in_thread(daemon=True, sleep_time=0.1)
