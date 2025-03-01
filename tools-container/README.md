# General in-cluster debug container

Note that the container currently does not contain k8s-specific tools.

## Using in Kubernetes

```bash
kubectl run -it --attach --rm --image bittrance/tools:latest bittrance-tools -- bash
```

## Building

```bash
docker build -t bittrance/tools:<version> tools-container/
docker push bittrance/tools:<version>
docker tag bittrance/tools:<version> bittrance/tools:latest
docker push bittrance/tools:latest
```
