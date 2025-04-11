# Simple TiDB setup

Default Kind setup. Tested with Kubernetes 1.31 and Kind 0.24.

```bash
kubectl create -f https://raw.githubusercontent.com/pingcap/tidb-operator/v1.6.1/manifests/crd.yaml
helm upgrade --install tidb-operator pingcap/tidb-operator --version v1.6.1 \
  --namespace tidb-admin \
  --create-namespace
kubectl apply -f ./tidb-cluster.yaml
```

Connect to TiDB (untested):

```bash
TIDB_IP=$(kubectl --namespace tidb-cluster get services hello-tidb-tidb -o jsonpath='{@.status.loadBalancer.ingress[0].ip}')
mysql -h $TIDB_IP --port 4000 -u root
```

## Setting up a reference mysql

```shell
docker run -d --rm --name mysql -p 127.0.0.1:3306:3306 -e MYSQL_ROOT_PASSWORD
='password' mysql:8.0
```

## Running qb tests

```shell
git clone https://github.com/winebarrel/qb
cd db
go install ./...
```

```shell
mysql -h $TIDB_IP --port 4000 -u root -e 'CREATE DATABASE sbtest'
qb --dsn "sbtest:password@tcp($TIDB_IP:4000)/sbtest" --initialize
qb --dsn "sbtest:password@tcp($TIDB_IP:4000)/sbtest"
```

## Running sysbench tests

Another useful db testing tool is [sysbench](https://github.com/akopytov/sysbench).

```shell
apt-get install sysbench
mysql -h $TIDB_IP --port 4000 -u root -e "
CREATE SCHEMA sbtest;
CREATE USER sbtest@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON sbtest.* to sbtest@'%';
"
sysbench \
  --db-driver=mysql \
  --threads=1 --time=60 \
  --mysql-host=$TIDB_IP \
  --mysql-port=4000 \
  --mysql-user=sbtest \
  --mysql-password=password /usr/share/sysbench/oltp_read_write.lua prepare
sysbench \
  --db-driver=mysql \
  --threads=1 --time=60 \
  --mysql-host=$TIDB_IP \
  --mysql-port=4000 \
  --mysql-user=sbtest \
  --mysql-password=password /usr/share/sysbench/oltp_read_write.lua run
```
