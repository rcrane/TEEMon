from flask import Flask, make_response
import getopt, sys, signal, os
import logging
from flask.logging import default_handler

app = Flask(__name__)

path="/sys/module/isgx/parameters/"

@app.route("/")
def main():
    return """<html>
			<head><title>SGX Exporter</title></head>
			<body>
			<h1>SGX Metrics</h1>
			<p><a href="/metrics">Metrics</a></p>
			</body>
			</html>"""


entries=[
    {'file': "sgx_nr_total_epc_pages", 
     'help': "total number of EPC pages reserved.",
     'type': "counter" },
    {'file': "sgx_nr_free_pages", 
     'help': "total number of currently free EPC pages.",
     'type': "counter"},
    {'file': "sgx_nr_low_pages", 
     'help': "minimum number of EPC pages before starting swapping.",
     'type': "counter"},
    {'file': "sgx_nr_high_pages", 
     'help': "number of free EPC pages above which we do not swap.",
     'type': "counter"},
    {'file': "sgx_nr_marked_old", 
     'help': "total number of EPC pages marked as old so far.",
     'type': "counter"},
    {'file': "sgx_nr_evicted", 
     'help': "total number of EPC pages that were evicted.",
     'type': "counter"},
    {'file': "sgx_nr_alloc_pages", 
     'help': "total number of EPC pages that were pulled back after eviction.",
     'type': "counter"},
    {'file': "sgx_nr_enclaves", 
     'help': "total number of Enclaves currently running.",
     'type': "counter"},
    {'file': "sgx_nr_reclaimed", 
     'help': "total number of EPC pages that were reclaimed.",
     'type': "counter"},
    {'file': "sgx_nr_added_pages", 
     'help': "total number of EPC pages that were added to enclaves.",
     'type': "counter"},
    {'file': "sgx_init_enclaves", 
     'help': "total number of Enclaves initialized.",
     'type': "counter"},
    {'file': "sgx_loaded_back", 
     'help': "total number of EPC pages loaded back from main memory.",
     'type': "counter"},
]

@app.route("/metrics")
def metrics():
    ret=""    
    for entry in entries:
        data="read error"
        with open(path+entry['file'], 'r') as myfile:
            data=myfile.read().replace('\n', '')
        ret += "# HELP {0} {1}\n# TYPE {0} {2}\n{0} {3}\n".format(entry['file'], entry['help'], entry['type'], data)
    response = make_response(ret)
    response.headers["content-type"] = "text/plain"

    return response

def usage():
    print("sgx_exporter.py: print SGX resource usage")
    print("-h, --help      print usage")
    print("-p, --path      set path of sgx module information")
    print("-v, --verbose   print some more information")


def sigterm(_signo, _stack_frame):
    print("sigterm: Exiting sgx_exporter.")
    sys.exit(0)

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:v", ["help", "path=", "verbose"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-p", "--path"):
            path = a
        else:
            assert False, "unhandled option"
    signal.signal(signal.SIGTERM, sigterm)
    
    # less messages
    app.logger.removeHandler(default_handler)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    app.run(host='0.0.0.0', port=int(os.getenv('LISTENING_PORT', '5000')))