# Backstage on Kubernetes demo

Experiment goals:

- Backstage running in Kubernetes
- Metadata from both CRD and repo scanning
- programmatic access to software catalog

# Setup

Set up Kind cluster including nginx ingress controller as per top-level instructions. Add cert-manager as per instructions in oidc federation experiment.

```shell
helm repo add backstage https://backstage.github.io/charts
helm upgrade --install backstage \
  --namespace backstage --create-namespace \
  --values ./backstage-k8s/backstage-values.yaml \
  backstage/backstage
kubectl --namespace backstage apply -f ./backstage-k8s/backstage-resources.yaml
```
