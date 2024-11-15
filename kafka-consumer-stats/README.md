# Experiment with Kafka

## Install Kafka

```shell
helm install kafka \
  --namespace kafka-cluster --create-namespace \
  --values ./kafka-cluster.yaml \
  oci://registry-1.docker.io/bitnamicharts/kafka
```

## Credentials for connecting to the cluster

```shell
echo """security.protocol=SASL_PLAINTEXT
sasl.mechanism=SCRAM-SHA-256
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
    username="user1" \
    password="$(kubectl get secret kafka-user-passwords --namespace kafka-cluster -o jsonpath='{.data.client-passwords}' | base64 -d | cut -d , -f 1)";
""" > ./client.properties
```

## Creating an example topic

```shell
kubectl apply -f ./kafka-admin.yaml

kubectl exec --namespace kafka-cluster kafka-admin -it -- /bin/bash -c 'kafka-topics.sh --bootstrap-server kafka.kafka-cluster.svc.cluster.local:9092  --command-config /work/client.properties --create --topic bittrance-test --partitions=10 --replication-factor=2'
```

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
