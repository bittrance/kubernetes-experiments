# Experiment with Kafka

## Install Kafka

See [Kafka on Kubernetes setup](../kafka-setup/README.md) for info on getting a Kafka cluster into Kind.

## Running from a remote cluster

The above commands create a dev environment to experiment and develop consumers, but you presumably want to run commands in production as well. Here is how you run the script:

```shell
kubectl cp ./consumer-poller.py kafka-admin:/root/consuer-poller.py
kubectl cp ./requirements.txt kafka-admin:/root/requirements.txt
kubectl exec --namespace kafka-cluster kafka-admin -it -- /bin/bash
apt-get update && apt-get install -y virtualenv
virtualenv ./venv
. ./venv/bin/activate
pip install -r ./requirements.txt
./offset-sampler.py --bootstrap-servers ze-kafka --interval 60 --sample-time 5 --jitter 10
```

## Table definition to load data into sqlite

```sql
CREATE TABLE stats (group_id VARCHAR, topic VARCHAR, partition INT, commit_rate INT, offset_delta INT);
.mode csv
.import ./offsets.csv stats
.save offset-stats.sqlite3
```
