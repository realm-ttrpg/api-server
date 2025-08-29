"""RPC module"""

# stdlib
import asyncio as aio
import json
import os
from uuid import uuid4

# 3rd party
from pydantic import BaseModel
from redis.asyncio import StrictRedis

# local
from realm_api.logging import logger
from .roll import roll_handler

redis_conn = StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"))
pubsub = redis_conn.pubsub(ignore_subscribe_messages=True)
handlers = {
    "roll": roll_handler,
}


async def init_pubsub() -> aio.Task:
    await pubsub.subscribe(**{"rpc.api": handler})
    return aio.create_task(pubsub.run())


async def shutdown_pubsub(task: aio.Task):
    await pubsub.unsubscribe()
    await pubsub.close()
    task.cancel()


async def handler(message: dict):
    """Handle an incoming RPC operation and publish the result."""

    data: dict = json.loads(message["data"])
    logger.info(f"Incoming RPC op: {data['uuid']} {data['op']}")
    result: BaseModel = await handlers[data["op"]](
        *data.get("args", []),
        **data.get("kwargs", dict()),
    )
    response = result.model_dump_json()
    await redis_conn.publish(data["uuid"], response)


async def rpc_bot(op: str, *args, timeout=3, **kwargs):
    """Perform an outgoing bot RPC operation and await the response."""

    q = aio.Queue()

    async def handler(message: dict):
        data = message["data"]
        await q.put(data)

    uuid = str(uuid4())
    await pubsub.subscribe(**{uuid: handler})
    message = {
        "uuid": uuid,
        "op": op,
        "args": args,
        "kwargs": kwargs,
    }
    logger.info(f"Outgoing RPC op: {message['uuid']} {message['op']}")

    try:
        await redis_conn.publish("rpc.bot", json.dumps(message))
        return await aio.wait_for(q.get(), timeout)

    finally:
        await pubsub.unsubscribe(uuid)
