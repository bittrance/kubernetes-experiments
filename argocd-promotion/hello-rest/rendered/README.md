
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/bittrance/kubernetes-experiments
# cd into the cloned directory
git checkout 3e9da8a959e43845bb3efad044c795d1260707d7
helm template . --name-template hello-rest-test --include-crds
```