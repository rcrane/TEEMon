# SGX statistics exporter

## Objective

Provide a simple way to export SGX related statistics such that these can be imported by prometheus.
One way would be to expand node_exporter. However, node_exporter is written in a verbose and generic fashion,
I prefer to write a little python-based webservice.

## Prerequisites

* You need to run the sgx_exporter on each node that provides SGX
  * We expanded the MONITORING repository accordingly
  * We provide a nice dashboard to visualize the SGX metrics

* We export this python web app as a container that runs as part of the MONITORING stack
  * This is based on 2.7-alpine


## Compilation and Execution

* Install the monitoring SGX driver:
  * `curl -fsSL https://raw.githubusercontent.com/scontain/SH/master/install_sgx_driver.sh | bash -s - install --force -p metrics `
* Create container:
  * `docker build -t sgx-exporter .`
  * `docker run --rm -p 5000:5000 -v /sys:/host/sys:ro sgx-exporter:latest`