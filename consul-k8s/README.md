# Consul on Kubernetes

Expose a Consul cluster:

```shell
helm repo add hashicorp https://helm.releases.hashicorp.com
helm upgrade consul hashicorp/consul \
  --install \
  --set global.name=consul \
  --set server.replicas=3 \
  --set server.exposeService.enabled=true \
  --namespace consul \
  --create-namespace
```

Call Consul's API:

```shell
IP=$(kubectl --namespace consul get services consul-expose-servers -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -v 'http://$IP:8500/v1/catalog/nodes'
```
