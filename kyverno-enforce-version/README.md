# Enforce release version numbers with Kyverno

This experiment strives to demonstrate how to use a Kyverno policy to stop deploys that have non-standard version numbers. The assumption is that builds on master branch are tagged and released with a traditional semver version, while builds from feature branches uses some other versioning scheme.

Create a standard Kind cluster as per top-level instructions.

```shell
helm upgrade --install kyverno kyverno/kyverno \
  --namespace kyverno --create-namespace \
  --set admissionController.replicas=3 \
  --set backgroundController.replicas=2 \
  --set cleanupController.replicas=2 \
  --set reportsController.replicas=2
```

Apply the policy:

```shell
kubectl apply -f ./kyverno-enforce-version/workload-policies.yaml
```

# Testing the policy:

We can use the canonical [./hello-rest](hello-rest) deployment which has no version and will thus not appease the rule:

```shell
kubectl create namespace hello-rest
kubectl label namespaces hello-rest windwards.net/namespace-type=workload
kubectl --namespace hello-rest apply -f ./hello-rest/hello-rest-deployment.yaml
```
