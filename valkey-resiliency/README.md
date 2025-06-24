# Resilient Valkey setup

## Creating a Valkey sentinel cluster

Set up a Kind cluster as per top-level instructions. Then install the Sentinel-based Valkey replica set:

```shell
helm upgrade --install \
  --namespace valkey-resiliency --create-namespace \
  --set architecture=replication \
  --set sentinel.enabled=true \
  --set sentinel.service.type=LoadBalancer \
  --set sentinel.primarySet=valkey-resiliency \
  --set sentinel.downAfterMilliseconds=10000 \
  --set sentinel.failoverTimeout=30000 \
  --set networkPolicy.allowExternal=false \
  valkey \
  oci://registry-1.docker.io/bitnamicharts/valkey
```

## Running the tests

```shell
PASSWORD=$(kubectl --namespace valkey-resiliency get secrets valkey -o jsonpath='{@.data.valkey-password}' | base64 -d)
kubectl --namespace valkey-resiliency run --image bittrance/tools:0.3.0 valkey-load -- sleep infinity
kubectl --namespace valkey-resiliency label pods valkey-load valkey-client=true
kubectl --namespace valkey-resiliency cp ./valkey-resiliency/valkey-load.js valkey-load:/root/
kubectl --namespace valkey-resiliency exec -it valkey-load -- k6 run -e REDIS_HOSTNAME=valkey -e REDIS_PRIMARYSET=valkey-resiliency -e REDIS_PASSWORD="$PASSWORD" /root/valkey-load.js
```

While the tests are running, restart Valkey:

```shell
kubectl --namespace valkey-resiliency rollout restart statefulset valkey-node
```

Currently, this fails occasionally, probably because the k6 redis client does not purge deleted pods fast enough.
