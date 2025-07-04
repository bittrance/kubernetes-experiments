
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/bittrance/kubernetes-experiments
# cd into the cloned directory
git checkout 5d64f80814181c645f7af653bf943e6fc845c461
helm template . --name-template hello-rest-test --include-crds
```