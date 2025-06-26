# Demonstrate Argo CD with environment promotion

Unlike other experiments, I decided it would be too much work to pull in my own SCM service (e.g. Forgejo) so you will have to modify this experiment to point to your own GitHub account or similar.

```shell
kind create cluster --config ./kind-cluster.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

## Setup Argo CD

```shell
helm --kube-context kind-test upgrade --install \
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

## Setup gitops-promoter

```shell
kubectl apply -f https://github.com/argoproj-labs/gitops-promoter/releases/download/v0.7.0/install.yaml
kubectl --namespace promoter-system create secret generic bittrance-gitops-promoter \
  --from-file=githubAppPrivateKey=./private-key.pem
```

I had to apply twice.

At this point, make sure your changes are pushed to SCM as this step will have ArgoCD start pulling from repo:

```yaml
kubectl apply -f ./argocd-promotion/apps.yaml
```

References:

- [argoproj-labs/gitops-promoter#332](https://github.com/argoproj-labs/gitops-promoter/pull/332)
