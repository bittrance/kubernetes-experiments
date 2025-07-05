
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/bittrance/kubernetes-experiments
# cd into the cloned directory
git checkout ed8ca9d80aeb665f4fcba4bd125805de3d783eb7
helm template . --name-template hello-rest-prod --set replicas=2 --include-crds
```