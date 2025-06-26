# Demonstrate Argo CD with environment promotion

This experiment demonstrates two  b

Unlike other experiments, I decided it would be too much work to pull in my own SCM service (e.g. Forgejo) so you will have to modify this experiment to point to your own GitHub account or similar.

```shell
kind create cluster --config ./kind-cluster.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

## Setup Argo CD

```shell
helm upgrade --install \
  --namespace argo-cd --create-namespace \
  --values ./argocd-promotion/values-argocd.yaml \
  argo-cd \
  argo/argo-cd
kubectl --namespace argo-cd create secret generic bittrance-gitops-promoter \
  --from-literal=url=https://github.com/bittrance/kubernetes-experiments \
  --from-literal=type=git \
  --from-literal=githubAppID=1460251 \
  --from-literal=githubAppInstallationID=72971609 \
  --from-file=githubAppPrivateKey=./private-key.pem
kubectl --namespace argo-cd label \
  secret bittrance-gitops-promoter \
  argocd.argoproj.io/secret-type=repository-write
```

There is currently an issue with the ArgoCD Helm chart which means it [cannot talk to the commit server](https://github.com/argoproj/argo-helm/issues/3333) because it uses default service name (argocd-commit-server vs argo-cd-argocd-commit-server). We can work around this issue by adding our own service with the expected name:

```shell
kubectl --namespace argo-cd apply -f argocd-promotion/commitserver-workaround.yaml
```

## Setup gitops-promoter

```shell
kubectl apply -f https://github.com/argoproj-labs/gitops-promoter/releases/download/v0.7.0/install.yaml
kubectl --namespace promoter-system create secret generic bittrance-gitops-promoter \
  --from-file=githubAppPrivateKey=./private-key.pem
```

I had to apply twice.

At this point, make sure your changes are pushed to SCM as this step will have ArgoCD start pulling from repo:

```yaml
kubectl apply -f ./argocd-promotion/platform-infra/team-awesome.yaml
```

References:

- [argoproj-labs/gitops-promoter#332](https://github.com/argoproj-labs/gitops-promoter/pull/332)
