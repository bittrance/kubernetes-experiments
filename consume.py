#!/usr/bin/env python3

import asyncio
import sys

from aiokafka import AIOKafkaConsumer, TopicPartition

async def consume(bootstrap_servers, group_id, auto):
    consumer = AIOKafkaConsumer(
        'bittrance-test',
        security_protocol='SASL_PLAINTEXT',
        sasl_mechanism='SCRAM-SHA-256',
        sasl_plain_username='user1',
        sasl_plain_password='w1ogDE4i8n',
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        enable_auto_commit=auto,
    )
    await consumer.start()
    await consumer.seek_to_end()
    try:
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
            if not auto:
                tp = TopicPartition(msg.topic, msg.partition)
                await consumer.commit({tp: msg.offset + 1})
    finally:
        await consumer.stop()

if __name__ == '__main__':
    asyncio.run(consume(sys.argv[1], sys.argv[2], sys.argv[3] == 'auto'))
