# Demonstrate an ingress middleware using Gateway API with Cilium

Tested with Kind 0.24.0 and Kubernetes 1.31.

```bash
kind create cluster --config ./gateway-api-cilium/kind-cluster-no-cni.yaml
docker run -d --rm --init --network kind -v /var/run/docker.sock:/var/run/docker.sock registry.k8s.io/cloud-provider-kind/cloud-controller-manager:v0.6.0
```

At the point of testing this, Cilium has a defect that means it fails to "adopt" gateways unless the `TLSRoute` CRD is present. To work around this, we load the experimental CRDs for now.

```bash
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.0/experimental-install.yaml
```

We can now install Cilium:

```bash
helm repo add cilium https://helm.cilium.io/
helm upgrade --install cilium cilium/cilium \
  --version 1.17.2 \
  --namespace kube-system \
  --set image.pullPolicy=IfNotPresent \
  --set ipam.mode=kubernetes \
  --set gatewayAPI.enabled=true \
  --set nodePort.enabled=true
```

We can now add an "interconnect":

```bash
kubectl apply -f ./gateway-api-cilium/gateway-api-interconnect.yaml
```
