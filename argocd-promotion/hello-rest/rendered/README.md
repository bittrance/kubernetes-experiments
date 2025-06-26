
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/bittrance/kubernetes-experiments
# cd into the cloned directory
git checkout 12e7afe638533d32a009497afe0c5f43e246126d
helm template . --name-template hello-rest-test --include-crds
```