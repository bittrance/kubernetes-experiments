# Demonstrate Argo CD with environment promotion

```shell
kind create cluster --config ./kind-cluster.yaml
kubectl --context kind-test apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

## Setup Argo CD

```shell
helm --kube-context kind-test upgrade --install \
  --namespace argo-cd --create-namespace \
  --values ./argocd-promotion/values-argocd.yaml \
  argo-cd \
  argo/argo-cd
```

```yaml
kubectl --context kind-test apply -f ./argocd-promotion/hello-world.yaml
```
