import http
import json
import os
from pprint import pprint as pp
from typing import List, re

from mitmproxy.certs import Cert
from mitmproxy.http import HTTPFlow
from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster

outupt_path = "output/requests.json"


class Addon(object):
    def __init__(self):
        dir = os.path.dirname(outupt_path)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        self.output = open(outupt_path, 'a')

    def request(self, flow: HTTPFlow):
        # do something in response
        pass

    def response(self, flow: HTTPFlow):
        if not ('aws' in flow.request.url or 'amazon' in flow.request.url):
            return

        resp_content_type = flow.response.headers.get('Content-Type')
        if not resp_content_type:
            return
        elif not 'json' in resp_content_type:
            return

        try:
            flow_data = {
                "request": {
                    "content_type": flow.response.headers.get('Content-Type'),
                    "url": flow.request.url,
                    "content": flow.request.content.decode(),
                },
                "response": {
                    "content_type": flow.response.headers.get('Content-Type'),
                    "status_code": flow.response.status_code,
                    "content": flow.response.content.decode(),
                }
            }
        except UnicodeDecodeError:
            pass
        self.output.write(json.dumps(flow_data))
        self.output.flush()

    def done(self):
        self.output.close()


class ProxyMaster(DumpMaster):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        try:
            DumpMaster.run(self)
        except KeyboardInterrupt:
            self.shutdown()


def start_proxy(host, port):
    paswd = os.getenv("CERT_PASSWORD")
    if not paswd:
        raise UserWarning("No CERT_PASSWORD env var")
    options = Options(
        listen_host=host,
        listen_port=port,
        http2=True,
        cert_passphrase=paswd
    )
    config = ProxyConfig(options)
    master = ProxyMaster(options, with_termlog=True, with_dumper=False)
    master.server = ProxyServer(config)
    master.addons.add(Addon())
    master.run()
