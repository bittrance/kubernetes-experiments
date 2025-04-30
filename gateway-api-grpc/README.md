# Experiement using Gateway API to get working grpc

The purpose of this experiment is to demonstrate L7 load balancing for grpc with Gateawy API.

## Set up a Kind cluster with Gateway API-enabled Cilium CNI

Follow the instructions in [Gateway API experiment with Cilium](../gateway-api-cilium/README.md). That doc uses a pre-release version. For the purpose of this experiment, a production release will do. I tested with 1.17.3.

A metrics server is also useful. See the top-level README for setup instructions.

## Install example grpc workload

```shell
kubectl apply -f ./gateway-api-grpc/hello-grpc.yaml
```

## Smoke test

```shell
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest
IP=$(kubectl --namespace hello-grpc \
    get services cilium-gateway-hello-grpc \
    -o jsonpath='{@.status.loadBalancer.ingress[0].ip}')
grpcurl -proto gateway-api-grpc/greetings.proto \
    -plaintext \
    -d '{"name": "Bittrance"}' \
    $IP:80 \
    greetings.GreetMe/Send
```

## Load test

```shell
env HELLO_GRPC_PLAINTEXT=true \
    HELLO_GRPC_ENDPOINT=$IP:80 \
    k6 run ./gateway-api-grpc/load-greetings.js
```

While this load test is running we can observe that the load is spread across all pods.

```shell
watch kubectl --context kind-kind --namespace hello-grpc top pods
```
