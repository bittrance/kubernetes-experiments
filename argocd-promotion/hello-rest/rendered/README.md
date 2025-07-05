
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/bittrance/kubernetes-experiments
# cd into the cloned directory
git checkout f389de220311338ee9dc93c65cd9470a8997923a
helm template . --name-template hello-rest-test --include-crds
```