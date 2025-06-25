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

We cheat slightly in this scenario in that we are reusing the hostname for the service that Cilium creates for our gateway `cilium-gateway-hello-grpc`. Actually, this service is an implementation detail and I suspect the name is not formally guaranteed to stay the same. However, we need a hostname for our TLS and the alternative would be to add e.g. external-dns to the mix.

## Smoke test

```shell
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest
grpcurl -proto gateway-api-grpc/greetings.proto \
    -insecure \
    -d '{"name": "Bittrance", "delay_ms": 2}' \
    cilium-gateway-hello-grpc.hello-grpc.test:443 \
    greetings.GreetMe/Send
```

## Load test

In the first iteration of this experiment, k6 grpc load test did not work, which turned out to be somehow related to using ALPN, see bug report [Gateway API with ALPN enbled won't GRPC](https://github.com/cilium/cilium/issues/39484). After some additional testing, it seems you need to add `appProtocol: kubernetes.io/h2c` to the backend Service definition. This seems a bit excessive given that the traffic is coming in via a Gateway that is known to terminate TLS and a GRPCRoute, but that's what it takes with current Cilium.

A simple load test using k6:

```shell
env HELLO_GRPC_ENDPOINT=cilium-gateway-hello-grpc.hello-grpc.test:443 \
    k6 run --insecure-skip-tls-verify \
        ./gateway-api-grpc/load-greetings.js
```

Here is the original [ghz](https://ghz.sh/) test:

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

Sample run. Note that the service is responsible for 1 ms:

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

While this load test is running we can observe that the load is spread across all pods, demonstrating L7 load balancing.

```shell
watch kubectl --namespace hello-grpc top pods
```

Note that the backend uses a 1 ms sleep, so this does not indicate max performance. Rather, it serves as a somewhat realistic indication of the overhead and spread you will get in a real-world scenario.
