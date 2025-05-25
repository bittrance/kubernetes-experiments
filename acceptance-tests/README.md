# Demonstration acceptance tests for Kubernetes setup

Over time, a platform team will undertake to provide quite a number of features in their clusters; think external-dns providing hostnames for certain resource attributes, kyverno stopping certain resource configurations, latency guarantees, and so on. As these accumulate, it will be hard to be sure that they all continue to work as designed.

For example, assuming the setup from [Gateway API waypoint proxy with Cilium](./gateway-api-cilium) how do we know that the setup is actually working in all the relevant ways?

This experiment demonstrates how to use [bats](https://bats-core.readthedocs.io/en/stable/) (and some common shell tools) to write acceptance tests for a Kubernetes configuration.

## Setup

Create a Kind cluster according to [Gateway API waypoint proxy with Cilium](./gateway-api-cilium). Add the cert-manager and DNS hack from [OIDC Federation with Dex](./oidc-federation).

Apart from `bats`, these tests assume your path contains `curl`, `host` (the DNS client from Bind) and `kubectl`.

```shell
bats ./acceptance-tests/tests.bats
```

The output looks something like this:

```text
tests.bats
 ✓ publishes a hostname
 ✓ redirects to HTTPS
 ✓ responds on HTTPS
 ✓ supports HTTPS on HTTP/2 (i.e. ALPN)

4 tests, 0 failures
```

