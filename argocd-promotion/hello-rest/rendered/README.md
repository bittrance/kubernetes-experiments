
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/bittrance/kubernetes-experiments
# cd into the cloned directory
git checkout 713064a4325ebb50c7004e7ce985a7d2279b8c54
helm template . --name-template hello-rest-prod --set replicas=3 --include-crds
```