# TeeMon

This repo contains the software for the paper "TEEMon: A continuous performance monitoring framework for TEEs"

https://dl.acm.org/doi/10.1145/3423211.3425677


## HowTo ##

* TeeMon requires the linux kernel to be of version 4.15.0-99 or newer. 
* Install dependencies: `docker-compose, docker.io, and linux-headers`
* Check if `/usr/src/linux-headers-$(uname -r)/include/uapi/linux/bpf_perf_event.h` is available on the host.
* Adapt user: `sudo adduser XXX docker`. Log out, log in.
* *Install the monitoring SGX driver*:
  * `curl -fsSL https://raw.githubusercontent.com/scontain/SH/master/install_sgx_driver.sh | bash -s - install --force -p metrics `
* Run: `./start.sh`
* Check running containers: `docker ps` should contain "prometheus, grafana, sgx-exporter, node-exporter, ebpf-exporter, cadvisor"
* Open: `http://localhost:9091`

## Remarks ##

* To adjust the dashboard open `http://localhost/login:9091` and login with `admin` and `adminadmin`
* Directly persisting your changes is not yet supported. Grafana will tell you to use the clipboard.
* You need to paste your changes into `grafana/provisioning/dashboards/*` and restart TeeMon

### SGX Dashboard ###

* On the SGX-Dashboard you need no use the "command filter" (top-left), eg. `*.redis.*` (regex) to show data in some of the graphs (eg. `Number of syscall_enter`).
* Be careful not to use `.*`. It will overload your browser!
* The `ebpf_exporter` curently tracks all processes.
* The "command filter" works on the first 16 characters of the process' command (similar to what `top` shows).
  

