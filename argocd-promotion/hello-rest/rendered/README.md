
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/bittrance/kubernetes-experiments
# cd into the cloned directory
git checkout ea57aa327fc9ce62cedd569a00812d133e4e81e3
helm template . --name-template hello-rest-test --include-crds
```