FROM ubuntu:24.10

RUN apt-get update && apt-get install --yes ca-certificates curl tcpdump valkey-tools netcat-openbsd bind9-host net-tools strace openssl gnupg neovim jq yq most

RUN gpg -k && \
    gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69 && \
    echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | tee /etc/apt/sources.list.d/k6.list && \
    apt-get update && \
    apt-get install k6

RUN curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.33/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg && \
    echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.33/deb/ /' | tee /etc/apt/sources.list.d/kubernetes.list && \
    apt-get update && \
    apt-get install --yes kubectl

RUN apt-get install --yes golang && \
    go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest && \
    ln -s /root/go/bin/grpcurl /usr/local/bin/grpcurl && \
    apt-get purge --yes golang && \
    apt-get autoremove --yes
