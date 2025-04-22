{
  "OAUTH2_PROXY_TLS_KEY_FILE": "/certs/tls.key",
  "OAUTH2_PROXY_TLS_CERT_FILE": "/certs/tls.crt",
  "OAUTH2_PROXY_UPSTREAMS": "http://localhost:8081/",
  "OAUTH2_PROXY_OIDC_ISSUER_URL": "https://dex.oidc-federation.test",
  "OAUTH2_PROXY_SSL_INSECURE_SKIP_VERIFY": "true",
  "OAUTH2_PROXY_PROVIDER": "oidc",
  "OAUTH2_PROXY_CLIENT_ID": .client_id,
  "OAUTH2_PROXY_CLIENT_SECRET": .client_secret,
  "OAUTH2_PROXY_REDIRECT_URL": "https://backend.oidc-federation.test",
  "OAUTH2_PROXY_SCOPE": "openid profile groups",
  "OAUTH2_PROXY_OIDC_EMAIL_CLAIM": "preferred_username",
  "OAUTH2_PROXY_CODE_CHALLENGE_METHOD": "S256",
  "OAUTH2_PROXY_COOKIE_SECRET": .cookie_secret,
  "OAUTH2_PROXY_PASS_AUTHORIZATION_HEADER": "true",
  "OAUTH2_PROXY_EMAIL_DOMAINS": "*"
}
| map_values(. | @base64)
| {
  "apiVersion": "v1",
  "kind": "Secret",
  "metadata": {
    "name": "oauth2-proxy"
  },
  "type": "Opaque",
  "data": .
}
