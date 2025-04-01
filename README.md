# Experiments with distributed workloads on Kubernetes

- [Kafka consumer stats](./kafka-consumer-stats): collect commit rate and offset rate for consumer groups on a Kafka cluster
- [Gateway API experiment with Cilium](./gateway-api-cilium): Attempt to create a waypoint proxy setup using Gateway API. Ultimately failed, but useful as a template.
- [General tools container](./tools-container): builds container image `bittrance/tools` useful for in-cluster debugging
- [Consul setup](./consul-k8s): sets up a Consul cluster on Kubernetes for testing and development
- [REST API testing container](./hello-rest): trivial REST API that can artificially delay requests

## Development setup

Most of these experiment assumes you have a local Kubernetes cluster set up.

```shell
kind create cluster --config ./kind-cluster.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
docker run -d --rm --network kind -v /var/run/docker.sock:/var/run/docker.sock registry.k8s.io/cloud-provider-kind/cloud-controller-manager:v0.4.0
```

## Set up Prometheus and Grafana in the cluster

```shell
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install observability \
  --namespace observability \
  --create-namespace \
  --values ./prometheus-stack-values.yaml \
  prometheus-community/kube-prometheus-stack
```
