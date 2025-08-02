# Loki setup

kind
ingress
cert-manager
kube-prometheus-stack

```shell
helm upgrade --install loki grafana/loki \
  --namespace loki --create-namespace \
  --values ./loki-log-aggregation/loki-values.yaml
kubectl apply --namespace loki -f ./loki-log-aggregation/certificate.yaml
```

```shell
echo l0calS3cr3t | htpasswd -i -c loki-tenants local-cluster
echo r3m0t3S3cr3t | htpasswd -i loki-tenants remote-cluster
kubectl --namespace loki create secret generic loki-tenants \
  --from-file=.htpasswd=./loki-tenants
```


```shell
helm upgrade --install fluent-bit fluent/fluent-bit \
  --namespace fluent-bit --create-namespace \
  --values ./loki-log-aggregation/fluent-bit-local-values.yaml
kubectl --namespace fluent-bit create secret generic fluent-bit \
  --from-literal=loki-passwd=l0calS3cr3t
```
