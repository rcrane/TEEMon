FROM python:3-alpine

#developed by Christof Fetzer "christof.fetzer@gmail.com"

RUN mkdir /SGX-Exporter

RUN cd /SGX-Exporter && \
    pip install flask 

COPY sgx_exporter.py /SGX-Exporter

CMD python /SGX-Exporter/sgx_exporter.py -p /host/sys/module/isgx/parameters/
