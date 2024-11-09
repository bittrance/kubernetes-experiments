# Experiment with Kafka

```shell
kind create cluster --config ./kind-cluster.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
docker run --rm --network kind -v /var/run/docker.sock:/var/run/docker.sock gcr.io/k8s-staging-kind/cloud-provider-kind:v0.4.0
```

```shell
helm install kafka \
  --namespace kafka-cluster --create-namespace \
  --values ./kafka-cluster.yaml \
  oci://registry-1.docker.io/bitnamicharts/kafka
```

```shell
kubectl get svc --namespace kafka-cluster
```

```shell
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install observability \
  --namespace observability \
  --create-namespace \
  --values ./prometheus-stack-values.yaml \
  prometheus-community/kube-prometheus-stack
```

```shell
echo """security.protocol=SASL_PLAINTEXT
sasl.mechanism=SCRAM-SHA-256
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
    username="user1" \
    password="$(kubectl get secret kafka-user-passwords --namespace kafka-cluster -o jsonpath='{.data.client-passwords}' | base64 -d | cut -d , -f 1)";
""" > ./client.properties
```

```shell
kubectl apply -f ./kafka-admin.yaml

kubectl exec --namespace kafka-cluster kafka-admin -it -- /bin/bash -c 'kafka-topics.sh --bootstrap-server kafka.kafka-cluster.svc.cluster.local:9092  --command-config /work/client.properties --create --topic bittrance-test --partitions=10 --replication-factor=2'
```
