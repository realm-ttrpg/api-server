"""RPC module"""

# stdlib
import asyncio as aio
import json
import os
from uuid import uuid4

# 3rd party
import redis

# api
from aethersprite import log

# local
from .roll import roll_handler

redis_conn = redis.StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"))
pubsub = redis_conn.pubsub(ignore_subscribe_messages=True)
handlers = {
    "roll": roll_handler,
}


def handler(message: dict):
    """Handle an incoming RPC operation and publish the result."""

    data = json.loads(message["data"])
    log.info(f"RPC op: {data['op']}")
    result = handlers[data["op"]](data)
    redis_conn.publish(data["uuid"], json.dumps(result))


async def rpc_bot(op: str, *args, timeout=3, **kwargs):
    """Perform an outgoing bot RPC operation and await the response."""

    q = aio.Queue()

    def handler(message: dict):
        data = json.loads(message["data"])
        aio.new_event_loop().run_until_complete(q.put(data))

    uuid = str(uuid4())
    pubsub.subscribe(**{uuid: handler})

    try:
        redis_conn.publish(
            "rpc.bot",
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
    pubsub.subscribe(**{"rpc.api": handler})
    pubsub.run_in_thread(daemon=True, sleep_time=0.01)


def teardown_webapp(*_):
    pubsub.unsubscribe()
    pubsub.close()
