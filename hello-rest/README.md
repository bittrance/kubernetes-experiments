# Demo REST API using gunicorn

## Deploying to a k8s cluster

```bash
kubectl apply -f ./hello-rest/hello-rest-deployment.yaml
```

## Building

```bash
docker build -t bittrance/hello-rest:<version> hello-rest/
docker push bittrance/hello-rest:<version>
```

## Testing locally

```bash
docker run --rm -p 127.0.0.1:8080:8080 --name hello-rest bittrance/hello-rest:<version>
```
# Testing graceful shutdown

gunicorn --workers=2 --bind unix:/tmp/sock --graceful-timeout 60 app:app

docker run --rm --name nginx -p 127.0.0.1:8080:8080 -v ./nginx.conf:/etc/nginx/nginx.conf -v /tmp/sock:/var/run/gunicorn.sock docker-hub.etraveli.net/docker/nginx-vts:1.18.0-3c6cf41

docker kill --signal=TERM nginx
docker kill --signal=QUIT nginx
