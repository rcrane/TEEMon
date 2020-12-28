#!/bin/bash

DRIVER_INSTALLED=$(lsmod | grep "isgx" | wc -l)

if [ $DRIVER_INSTALLED -ge 1 ]; then
        echo "SGX driver installed!"
else
        echo "SGX driver NOT installed!" 
fi

docker build -t ebpf_exporter ./exporters/ebpf_exporter
docker build -t sgx_exporter  ./exporters/sgx_exporter

cd prometheus
if [ -d "storage" ]; then
	# enable for auto backup upon start
	# TMPDIR=$(mktemp -d -p . XXXXXXX)
	# mv storage/* $TMPDIR/ 
	echo "re-using old storage dir"
else
	mkdir storage
fi
cd ..

CURRENT_UID=$(id -u):$(id -g) docker-compose up -d

echo "You may now open http://localhost:9091"


