
FROM golang:1.16.0-buster as builder

# Doing mostly what CI is doing here
RUN apt-get -q update && apt-get -q upgrade -y
RUN apt-get -q autoremove
RUN apt-get install -y -q apt-transport-https apt-utils linux-headers-amd64 cmake llvm libelf-dev libclang-dev bison flex python zlib1g-dev luajit build-essential arping libluajit-5.1-dev apt-utils iperf git autotools-dev automake autogen

RUN git clone https://github.com/HewlettPackard/netperf.git
RUN cd netperf && ./autogen.sh && ./configure && make -j4 &&  make install

RUN curl -sL https://github.com/iovisor/bcc/releases/download/v0.18.0/bcc-src-with-submodule.tar.gz | tar xvz  -C  /tmp/

RUN cd /tmp/bcc && cmake . && make -j4 && make install

COPY ./ /go/ebpf_exporter

RUN cd /go/ebpf_exporter && go mod vendor && go mod download && GOPATH="" GOPROXY="off" GOFLAGS="-mod=vendor" go install -v ./...
# go mod download


# Create a small container to execute the ebpf exporter

#FROM debian:stretch-slim

#RUN apt-get update && apt-get -y autoremove 

#RUN apt-get install -y gnupg

#RUN apt-get install -y apt-transport-https && \
#    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 648A4A16A23015EEF4A66B8E4052245BD4284CDD && \
#    echo "deb https://repo.iovisor.org/apt/xenial xenial main" > /etc/apt/sources.list.d/iovisor.list && \
#    apt-get update && \
#    apt-get install -y libbcc linux-headers-amd64 
RUN ls -r /root/go/bin/ebpf_exporter
RUN cp /root/go/bin/ebpf_exporter /usr/bin/ebpf_exporter

COPY ./configfile/sgx.yaml /etc/ebpf_exporter/

ENTRYPOINT [ "ebpf_exporter" ]
CMD [ "--config.file=/etc/ebpf_exporter/sgx.yaml" ]


# run as privileged!

# mount this:
# /lib/modules:/lib/modules:ro
# /sys:/sys:ro
# /usr/src:/usr/src:ro

# map this port:
# 9435:9435
