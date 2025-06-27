
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/bittrance/kubernetes-experiments
# cd into the cloned directory
git checkout fc30edeea761fa9b6413a0d8ff67fcfab774c06b
helm template . --name-template hello-rest-test --include-crds
```