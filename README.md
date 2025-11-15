# Experiments with distributed workloads on Kubernetes

- [Kafka consumer stats](./kafka-consumer-stats): collect commit rate and offset rate for consumer groups on a Kafka cluster
- [Gateway API waypoint proxy with Cilium](./gateway-api-cilium): Attempt to create a waypoint proxy setup using Gateway API. Ultimately failed, but useful as a template.
- [Gateway API GRPC load balancing](./gateway-api-grpc): Use Gateway API and Cilium to get L7 load balancing of GRPC requests.
- [TiDB benchmarking](./tidb-benchmarks): Set up a three-node TiDB cluster and benchmark it with various methods.
- [General tools container](./tools-container): builds container image `bittrance/tools` useful for in-cluster debugging
- [Consul setup](./consul-k8s): sets up a Consul cluster on Kubernetes for testing and development
- [REST API testing container](./hello-rest): trivial REST API that can artificially delay requests
- [Enforce release versions with Kyverno](./kyverno-enforce-verions): Simple Kyverno rule to ensure deployed workload version numbers follow a certain pattern.
- [Resilient Valkey setup](./valkey-resiliency): Demonstrate the resiliency of a Sentinel-based Valkey setup, using a k6 load test

## Development setup

Most of these experiment assumes you have a local Kubernetes cluster set up.

```shell
kind create cluster --config ./kind-cluster.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
docker run -d --rm \
  --name cloud-provider-kind \
  --network kind \
  -v /var/run/docker.sock:/var/run/docker.sock \
  registry.k8s.io/cloud-provider-kind/cloud-controller-manager:v0.4.0
```

## Add a metrics-server

```shell
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.7.2/components.yaml
kubectl patch deployments.apps --namespace kube-system metrics-server --type=json --patch '[{"op": "add", "path": "/spec/template/spec/containers/0/args/2", "value": "--kubelet-insecure-tls"}]'
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

## Add users with RBAC

Generate a private key and a CSR for the user:
```shell
openssl genrsa -out bittrance.key 2048
openssl req -new -key bittrance.key -out bittrance.csr -subj "/CN=bittrance/O=developers"
```

Given the CSR, and admin can now ask Kubernetes to sign the request:

```shell
CSR_DATA=$(base64 -w0 < bittrance.csr)
echo "apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: bittrance
spec:
  request: $CSR_DATA
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 604800
  usages:
    - client auth" | kubectl apply -f -
kubectl certificate approve bittrance
kubectl get csr bittrance -o jsonpath='{ .status.certificate }' | base64 -d > bittrance.crt
```

In order for bittrance to be able to perform actions, we need some RBAC:

```shell
kubectl apply -f ./util-manifests/bittrance-rbac.yaml
```

With this certificate, we can now create a kubectl context:

```shell
kubectl config set-credentials bittrance \
  --client-key=bittrance.key \
  --client-certificate=bittrance.crt \
  --embed-certs=true
kubectl config set-context kind-bittrance --cluster kind-kind --user bittrance
kubectl --context kind-bittrance get deployments -A
```
