{
  "replicaCount": 2,
  "podDisruptionBudget": {
    "enabled": true,
    "minAvailable": 1
  },
  "https": {
    "enabled": true
  },
  "service": {
    "type": "LoadBalancer",
    "ports": {
      "http": {
        "port": 80
      },
      "https": {
        "port": 443
      }
    }
  },
  "volumes": [
    {
      "name": "secret-volume",
      "secret": {
        "secretName": "dex-certificate"
      }
    }
  ],
  "volumeMounts": [
    {
      "name": "secret-volume",
      "readOnly": true,
      "mountPath": "/certs"
    }
  ],
  "config": {
    "issuer": "https://dex.oidc-federation.test",
    "web": {
      "tlsCert": "/certs/tls.crt",
      "tlsKey": "/certs/tls.key"
    },
    "logger": {
      "format": "json"
    },
    "storage": {
      "type": "kubernetes",
      "config": {
        "inCluster": true
      }
    },
    "connectors": [
      {
        "type": "oidc",
        "id": "bittrancegmailcom",
        "name": "oidc-federation",
        "config": {
          "issuer": "https://login.microsoftonline.com/0a3a19f8-5fe4-4fb1-aabc-2bf971085ba2/v2.0",
          "clientID": .appId,
          "clientSecret": .password,
          "redirectURI": "https://dex.oidc-federation.test/callback",
          "insecureSkipEmailVerified": true,
          "insecureEnableGroups": true
        }
      }
    ],
    "staticClients": [
      {
        "id": .client_id,
        "name": "backend",
        "redirectURIs": [
          "https://backend.oidc-federation.test/oauth2/callback"
        ],
        "secret": .client_secret
      }
    ]
  }
}
