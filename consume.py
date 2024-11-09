#!/usr/bin/env python3

import asyncio
import sys

from aiokafka import AIOKafkaConsumer

async def consume(bootstrap_servers, group_id):
    consumer = AIOKafkaConsumer(
        'bittrance-test',
        security_protocol='SASL_PLAINTEXT',
        sasl_mechanism='SCRAM-SHA-256',
        sasl_plain_username='user1',
        sasl_plain_password='w1ogDE4i8n',
        bootstrap_servers=bootstrap_servers,
        group_id=group_id)
    await consumer.start()
    try:
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        await consumer.stop()

if __name__ == '__main__':
    asyncio.run(consume(sys.argv[1], sys.argv[2]))
