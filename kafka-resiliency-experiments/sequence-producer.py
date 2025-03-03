#!/usr/bin/env python3

import argparse
import asyncio
import contextlib
import csv
import random
import sys
import time

from aiokafka import AIOKafkaProducer

async def sample_offsets(cb, sample_time, **kafka_config):
    kafka_config['group_id'] = 'andqvi-consumer-poller'
    consumer = AIOKafkaConsumer(
        '__consumer_offsets',
        **kafka_config,
    )
    await consumer.start()
    await consumer.seek_to_end()
    deadline = time.time() + sample_time
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
            if time.time() > deadline:
                break
    finally:
        await consumer.stop()


def args():
    parser = argparse.ArgumentParser(
        prog='consumer-poller',
        description='Collects statistics on consumer group offsets',
    )
    parser.add_argument('--bootstrap-servers', dest='bootstrap_servers')
    parser.add_argument('--username', dest='sasl_plain_username')
    parser.add_argument('--password', dest='sasl_plain_password')
    parser.add_argument('--interval', type=float, dest='sampling_interval', default=10)
    parser.add_argument('--sample-time', type=float, dest='sample_time', default=2)
    parser.add_argument('--jitter', type=float, dest='sampling_jitter', default=2)
    args = vars(parser.parse_args())
    for k in list(args.keys()):
        if k is None:
            del args[k]
    return args

if __name__ == '__main__':
    kafka_config = args()
    if kafka_config.get('sasl_plain_username'):
        kafka_config.update({
            'security_protocol': 'SASL_PLAINTEXT',
            'sasl_mechanism': 'SCRAM-SHA-256',
        })
    sampler_config = { key: kafka_config.pop(key) for key in ['sampling_interval', 'sample_time', 'sampling_jitter'] }
    asyncio.run(runner(kafka_config, sampler_config))

