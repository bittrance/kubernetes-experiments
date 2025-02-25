# Set up Kafka cluster for Kubernetes experiments

## Install Kafka

```shell
helm install kafka \
  --namespace kafka-cluster --create-namespace \
  --values ./kafka-cluster-values.yaml \
  oci://registry-1.docker.io/bitnamicharts/kafka
```

## Set up typical dashboard for Kafka

```shell
kubectl apply -f ./kafka-setup/kafka-dashboard.yaml
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
