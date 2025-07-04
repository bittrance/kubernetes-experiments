
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/bittrance/kubernetes-experiments
# cd into the cloned directory
git checkout c7e61e03532c2a8b607300f88b5e487b2cabb329
helm template . --name-template hello-rest-prod --include-crds
```