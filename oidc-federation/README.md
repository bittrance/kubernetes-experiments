# Federated OIDC with Dex

Standard Kind cluster setup. Include ingress controller.

## Get a shared DNS view for development

When working with a combination of internal and external clients that care about domain names, we need both sides to to be able to resolve names that are assigned to services. This recipe will set up the TLD `.test` so that all LoadBalancer services will be registered under this domain in addition to `svc.cluster.local`.

Edit the coredns configmap and add `k8s_external test` inside the braces. The format of this config makes it hard to write a snazzy commandline to update it:

```shell
kubectl --namespace kube-system edit configmaps coredns
```

Then switch the kube-dns service over to a LoadBalancer service so that it can be reached from outside the cluster:

```shell
kubectl --namespace kube-system patch service kube-dns --type=json --patch='[{"op": "add", "path": "/spec/type", "value": "LoadBalancer"}]'
```

Finally, add the LoadBalancer IP to the local DNS configuration:

```shell
kubectl --namespace kube-system get services kube-dns -o jsonpath='{@.status.loadBalancer.ingress[0].ip}'
sudo vi /etc/systemd/resolved.conf
```

## Set up cert-manager for TLD .test

```shell
helm repo add jetstack https://charts.jetstack.io
helm upgrade --install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.17.0 \
  --set crds.enabled=true
```

```shell
kubectl apply -f ./oidc-federation/selfsigned-ca.yaml
```

## Install dex

```shell
helm repo add dex https://charts.dexidp.io
helm upgrade --install dex dex/dex \
  --namespace oidc-federation \
  --create-namespace \
  --value ./oidc-federation/dex-values.yaml
kubectl --namespace oidc-federation apply -f ./oidc-federation/dex-certificate.yaml
```
