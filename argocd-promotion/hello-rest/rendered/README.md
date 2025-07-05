
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/bittrance/kubernetes-experiments
# cd into the cloned directory
git checkout 3b911e91d4c6b078b5bf78a2e44ed30799f756d9
helm template . --name-template hello-rest-test --include-crds
```