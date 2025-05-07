# Experiement using Gateway API to get working grpc

The purpose of this experiment is to demonstrate L7 load balancing for grpc with Gateway API.

## Set up a Kind cluster with Gateway API-enabled Cilium CNI

Follow the instructions in [Gateway API waypoint proxy with Cilium](../gateway-api-cilium/README.md) to create a cluster with Cilium and Gateway API support, including exposing coredns. That doc uses a pre-release version. For the purpose of this experiment, a production release will do. I tested with 1.17.3.

We need certificate support to get TLS for our GPRC service. Follow instructions in [Federated OIDC with Dex](./oidc-federation/README.md).

A metrics server is also useful. See the top-level README for setup instructions.

## Install example grpc workload

Let's install an example grpc service from [bittrance/hello-world](https://hub.docker.com/repository/docker/bittrance/hello-world/general).

```shell
kubectl apply -f ./gateway-api-grpc/hello-grpc.yaml
```

## Smoke test

```shell
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest
grpcurl -proto gateway-api-grpc/greetings.proto \
    -insecure \
    -d '{"name": "Bittrance", "delay_ms": 2}' \
    hello-grpc.hello-grpc.test:443 \
    greetings.GreetMe/Send
```

## Load test

For unclear reasons, possibly because this setup seems not to support ALPN, k6/net/grpc does not work. We use [ghz](https://ghz.sh/) instead:

```shell
ghz --cpus 4 \
    --duration 60s \
    --connections 5 \
    --rps 100 \
    --proto greetings.proto \
    -d '{"name": "Bittrance", "delay_ms": 1}' \
    --call greetings.GreetMe/Send \
    --skipTLS \
    cilium-gateway-hello-grpc.hello-grpc.test:443
```

Sample run:

```
Latency distribution:
  10 % in 3.02 ms
  25 % in 3.13 ms
  50 % in 3.28 ms
  75 % in 3.45 ms
  90 % in 3.63 ms
  95 % in 3.75 ms
  99 % in 4.03 ms
```

While this load test is running we can observe that the load is spread across all pods.

```shell
watch kubectl --context kind-kind --namespace hello-grpc top pods
```
