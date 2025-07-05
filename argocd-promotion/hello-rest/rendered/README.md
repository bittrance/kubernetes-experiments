
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/bittrance/kubernetes-experiments
# cd into the cloned directory
git checkout 4b4b52fce14efe898531b923aca3cb7a9af8a8c7
helm template . --name-template hello-rest-test --include-crds
```