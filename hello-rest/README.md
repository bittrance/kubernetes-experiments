# Demo REST API using gunicorn

This example REST API uses [bittrance/hello-world](https://github.com/bittrance/hello-world). It is primarily meant as a demonstration workload for use with other experiments.

## Deploying to a k8s cluster

```bash
kubectl apply -f ./hello-rest/deployment.yaml
```

## Running the load test

```bash
IP=$(kubectl --namespace hello-rest get services hello-rest -o jsonpath='{@.status.loadBalancer.ingress[0].ip}')
env HELLO_REST_ENDPOINT=http://$IP:8080 k6 run ./hello-rest/load-test.js
```
