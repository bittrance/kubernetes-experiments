# Loki setup

This experiment has two goals:

- demonstrate app log aggregation with [Loki](https://grafana.com/oss/loki/). I node and infra logs are out of scope.
- demonstrate how to produce log entries that are reasonably compact and easy to work with. For example, many log collectors annotate logs with every label available, leading to lots of noise in the log presentation.

# Setup

Create a standard Kind cluster as per top-level instructions. Add ingress controller. Set up cert-manager according to instructions in [Federated OIDC with Dex](./oidc-federation/README.md).

Install kube-prometheus-stack per top-level instructions so we have somewhere to view logs.

We can now install Loki:

```shell
helm upgrade --install loki grafana/loki \
  --namespace loki --create-namespace \
  --values ./loki-log-aggregation/loki-values.yaml
kubectl apply --namespace loki -f ./loki-log-aggregation/certificate.yaml
```

The OSS version of the Loki stack depends on nginx and using an ordinary htpasswd file for access. The local-cluster user is used both by fluent-bit below and by the loki-canary helper that verifies that logs flow correctly from all nodes:

```shell
export LOCAL_PASSWD=l0calS3cr3t
export READER_PASSWD=datas0urc3
echo $LOCAL_PASSWD | htpasswd -i -c loki-tenants local-cluster
echo $READER_PASSWD | htpasswd -i loki-tenants reader
kubectl --namespace loki create secret generic loki-tenants \
  --from-file=.htpasswd=./loki-tenants
```

We can now add a fluent-bit setup that ships its logs to Loki in the local cluster:

```shell
helm upgrade --install fluent-bit fluent/fluent-bit \
  --namespace fluent-bit --create-namespace \
  --values ./loki-log-aggregation/fluent-bit-local-values.yaml
kubectl --namespace fluent-bit create secret generic fluent-bit \
  --from-literal=loki-passwd=$LOCAL_PASSWD
```

We can now create a datasource under https://grafana.localtest.me/ using the reader user with the password above. Logs should have the labels `namespace`, `service_name` and `container` and various structured metadata properties such as container image.
