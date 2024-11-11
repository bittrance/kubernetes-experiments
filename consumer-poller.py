#!/usr/bin/env python3

import asyncio
import contextlib
import csv
import sys
import time

from aiokafka import AIOKafkaConsumer, TopicPartition

def parse_key(key):
    group_id_field_start = 3
    group_id_data_start = 4
    group_id_len = key[group_id_field_start]
    group_id = key[group_id_data_start:(group_id_data_start + group_id_len)]
    topic_field_start = group_id_data_start + group_id_len + 1
    topic_data_start = topic_field_start + 1
    topic_len = key[topic_field_start]
    topic = key[topic_data_start:(topic_data_start + topic_len)]
    partition = int.from_bytes(key[-2:], 'big', signed=True)
    return (group_id.decode("utf-8"), topic.decode("utf-8"), partition)


async def poll_offsets(cb, **kafka_config):
    kafka_config['group_id'] = 'andqvi-consumer-poller'
    consumer = AIOKafkaConsumer(
        '__consumer_offsets',
        **kafka_config,
    )
    await consumer.start()
    await consumer.seek_to_end()
    try:
        async for msg in consumer:
            try:
                group_id, topic, partition = parse_key(msg.key)
            except:
                sys.stderr.write(f"Unparseable message key {msg.key}\n")
                continue
            offset = int.from_bytes(msg.value[2:10], 'big', signed=True)
            if topic != '__consumer_offsets':
                cb(group_id, topic, partition, time.time(), offset)
    finally:
        await consumer.stop()


async def runner(**kafka_config):
    output = csv.writer(sys.stdout)
    output.writerow(['tstamp', 'group_id', 'topic', 'partition', 'offset_delta'])
    consumer_groups = {}
    def receiver(group_id, topic, partition, tstamp, offset):
        group = consumer_groups.setdefault(group_id, {'topics': {}})
        topic_stats = group['topics'].setdefault(f'{topic}/{partition}',  {'latest_offset': None})
        latest_offset = topic_stats['latest_offset'] 
        delta = None if latest_offset is None else offset - latest_offset
        topic_stats['latest_offset'] = offset
        output.writerow([int(tstamp), group_id, topic, partition, delta])

    while True:
        async with asyncio.TaskGroup() as tasks:
            tasks.create_task(poll_offsets(receiver, **kafka_config))
            tasks.create_task(asyncio.sleep(1))
        await asyncio.sleep(10)


if __name__ == '__main__':
    kafka_config = {
        'bootstrap_servers': sys.argv[1],
        'security_protocol': 'SASL_PLAINTEXT',
        'sasl_mechanism': 'SCRAM-SHA-256',
        'sasl_plain_username': 'user1',
        'sasl_plain_password': 'w1ogDE4i8n',
    }
    asyncio.run(runner(**kafka_config))

