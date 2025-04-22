# Federated OIDC with Dex

Standard Kind cluster setup. Include ingress controller.

## Get a shared DNS view for development

When working with a combination of internal and external clients that care about domain names, we need both sides to to be able to resolve names that are assigned to services. This recipe will set up the TLD `.test` so that all LoadBalancer services will be registered under this domain in addition to `svc.cluster.local`.

Edit the coredns configmap and add `k8s_external test` inside the braces. The format of this config makes it hard to write a snazzy commandline to update it:

```shell
kubectl --namespace kube-system edit configmaps coredns
```

Then switch the kube-dns service over to a LoadBalancer service so that it can be reached from outside the cluster:

```shell
kubectl --namespace kube-system patch service kube-dns --type=json --patch='[{"op": "add", "path": "/spec/type", "value": "LoadBalancer"}]'
```

Finally, add the LoadBalancer IP to the local DNS configuration:

```shell
kubectl --namespace kube-system get services kube-dns -o jsonpath='{@.status.loadBalancer.ingress[0].ip}'
sudo vi /etc/systemd/resolved.conf
```

## Set up cert-manager for TLD .test

```shell
helm repo add jetstack https://charts.jetstack.io
helm upgrade --install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.17.0 \
  --set crds.enabled=true
kubectl apply -f ./oidc-federation/selfsigned-ca.yaml
```

## Install dex

First step is to create an Enterprise app and service principal. I had problem running the azcli commands below because some of them failed with JSON decode errors. Attaching `--output tsv` solves that issue but the creds json will have to be constructed by hand.

```shell
docker run -d --rm --name azcli -it -v .:/work mcr.microsoft.com/azure-cli:cbl-mariner2.0 bash -c 'sleep 3600'
docker exec -it azcli az login --use-device-code
docker exec azcli \
  az ad app create \
    --display-name oidc-federation \
    --web-redirect-uris https://dex.oidc-federation.test/callback \
    --optional-claims /work/oidc-federation/optional-claims.json \
    --required-resource-accesses /work/oidc-federation/required-resources.json
APPID=$(docker exec azcli \
  az ad app list --display-name oidc-federation --query '[0].appId' --output tsv)
docker exec azcli \
  az ad app update --id $APPID --set groupMembershipClaims=SecurityGroup
docker exec azcli \
  az ad sp create --id $APPID
docker exec azcli \
  az ad sp credential reset --id $APPID \
    --end-date $(date +%Y-%m-%dT%H:%M:%S%z --date '1 months') > dex-client.json
```

We also need to generate a client for our backend that we can then inject into Dex and backend:

```shell
echo "{
\"client_id\": \"$(uuidgen)\",
\"client_secret\": \"$(pwgen -s 32)\",
\"cookie_secret\": \"$(pwgen -s 32)\"
}" | jq . > oauth2-proxy-client.json
cat dex-client.json oauth2-proxy-client.json \
  | jq -s add \
  | yq -y -f ./oidc-federation/dex-values.jq \
  > ./oidc-federation/dex-values.yaml
cat oauth2-proxy-client.json \
  | jq -f ./oidc-federation/oauth2-proxy-config.jq \
  > ./oidc-federation/oauth2-proxy-config.yaml
```

We can now install Dex and provide it with a cert from our self-signed CA:

```shell
helm repo add dex https://charts.dexidp.io
helm upgrade --install dex dex/dex \
  --namespace oidc-federation \
  --create-namespace \
  --values ./oidc-federation/dex-values.yaml
kubectl --namespace oidc-federation apply -f ./oidc-federation/dex-certificate.yaml
```

## Install backend

Manifest needs manually adding client id, secret for now.

```shell
kubectl --namespace oidc-federation apply \
  -f ./oidc-federation/backend.yaml \
  -f ./oidc-federation/oauth2-proxy-config.yaml
```

At this point, navigating to [https://backend.oidc-federation.test](https://backend.oidc-federation.test ) should start login flow.
