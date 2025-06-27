
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/bittrance/kubernetes-experiments
# cd into the cloned directory
git checkout 4051ca26c0d20e61c9ff4bb23f76d945786486c6
helm template . --name-template hello-rest-prod --include-crds
```