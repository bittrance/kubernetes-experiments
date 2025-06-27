
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/bittrance/kubernetes-experiments
# cd into the cloned directory
git checkout 966abe1c9854d61ffc70d2895e9bb2229cfae46e
helm template . --name-template hello-rest-prod --include-crds
```