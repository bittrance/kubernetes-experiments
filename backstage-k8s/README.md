# Backstage on Kubernetes demo

helm repo add backstage https://backstage.github.io/charts
helm upgrade --install backstage \
  --namespace backstage --create-namespace \
  --set backstage.pdb.create=true \
  --set ingress.enabled=true \
  --set ingress.host=backstage.localtest.me \
  --set ingress.tls.enabled=true \
  --set ingress.tls.secretName=backstage-certificate \
  backstage/backstage

  --set backstage.replicas=2 \
  --set postgresql.enabled=true \

cert-manager.

kubectl --namespace backstage apply -f ./backstage-k8s/certificate.yaml
