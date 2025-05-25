HELLO_HOSTNAME=${HELLO_HOSTNAME:-cilium-gateway-hello-test.hello-test.test}
KUBECTL=${KUBECTL:-kubectl --context kind-kind}

setup_file() {
	$KUBECTL apply -f ./acceptance-tests/hello-test.yaml	
}

teardown_file() {
	$KUBECTL delete namespace hello-test	
}

timeout() {
	local wait_time=$1
	shift
	local start=$(date +%s)
	while ! $* ; do
		local now=$(date +%s)
		if [ $((now - start)) -gt $wait_time ] ; then
			echo "Timeout trying $*" >&2
			return 1
		fi
		echo -n "."
		sleep 5
	done
}

@test "publishes a hostname" {
	timeout 60 host $HELLO_HOSTNAME
}

@test "redirects to HTTPS" {
	local location=$(curl -fs -I -w '%header{location}' -o /dev/null http://$HELLO_HOSTNAME)
	echo $location | grep -E '^https:'
}

@test "responds on HTTPS" {
	curl --insecure -f -o /dev/null https://$HELLO_HOSTNAME
}

@test "supports HTTPS on HTTP/2 (i.e. ALPN)" {
	curl --http2 --insecure -f -o /dev/null https://$HELLO_HOSTNAME
}
