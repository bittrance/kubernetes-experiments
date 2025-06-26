
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/bittrance/kubernetes-experiments
# cd into the cloned directory
git checkout 668848e070441ea8c01aa03fb15387ab1b82b5cc
helm template . --name-template hello-rest-prod --include-crds
```