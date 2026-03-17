# Marimo on Kubernetes

We need a Kind cluster:

```shell
kind create cluster --config kind-cluster.yaml
```

In order to expose our notebooks outside the cluster, we need an ingress controller:

```shell
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

We can now install the Marimo operator. The manifest seems not to be published so I have copied the manifest locally for now:

```shell
kubectl apply -f marimo/manifest.yaml
```

Once the CRD is loaded, we can set up an example notebook:

```shell
kubectl apply -f marimo/examples.yaml
```

This should allow you to point your browser to http://marimo-examples.localtest.me/ with password `verrah-s3cr3t`.
