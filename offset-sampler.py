#!/usr/bin/env python3

import argparse
import asyncio
import contextlib
import csv
import random
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


async def runner(kafka_config, config):
    output = csv.writer(sys.stdout)
    output.writerow(['tstamp', 'group_id', 'topic', 'partition', 'offset_delta'])

    stats = {}
    def receiver(group_id, topic, partition, tstamp, offset):
        entry = stats.setdefault((group_id, topic, partition),  {'latest_offset': None, 'commits': 0})
        entry['latest_offset'] = offset
        entry['commits'] += 1

    prev_offsets = {}
    def cycle_stats(sample_fraction):
        for key, entry in stats.items():
            group_id, topic, partition = key
            prev_offset = prev_offsets.get(key)
            delta = None if prev_offset is None else entry['latest_offset'] - prev_offset
            estimated_commits = entry['commits'] * sample_fraction
            output.writerow([group_id, topic, partition, estimated_commits, delta])
            prev_offsets[key] = entry['latest_offset']
        stats.clear()

    while True:
        start = time.time()
        await sample_offsets(receiver, config['sample_time'], **kafka_config)
        cycle_stats(config['sampling_interval'] / config['sample_time'])
        sys.stdout.flush()
        elapsed = time.time() - start
        if config['sampling_interval'] < elapsed:
            sys.stderr.write(f'sampling took too long: {elapsed}s\n')
        else:
            jitter = random.random() * config['sampling_jitter'] - config['sampling_jitter'] / 2
            await asyncio.sleep(config['sampling_interval'] - elapsed + jitter)


def args():
    parser = argparse.ArgumentParser(
        prog='consumer-poller',
        description='Collects statistics on consumer group offsets',
    )
    parser.add_argument('--bootstrap-servers', dest='bootstrap_servers')
    parser.add_argument('--username', dest='sasl_plain_username')
    parser.add_argument('--password', dest='sasl_plain_password')
    parser.add_argument('--interval', dest='sampling_interval', default=10)
    parser.add_argument('--sample-time', dest='sample_time', default=2)
    parser.add_argument('--jitter', dest='sampling_jitter', default=2)
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

