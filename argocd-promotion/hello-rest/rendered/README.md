
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/bittrance/kubernetes-experiments
# cd into the cloned directory
git checkout 040e8ac38e4fe00a84bfb0c709d79a553ffad568
helm template . --name-template hello-rest-test --set replicas=3 --include-crds
```