import http
import json
import os
from pprint import pprint as pp
from typing import List, re

from mitmproxy.http import HTTPFlow
from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster

outupt_path = "output/requests.json"


class Addon(object):
    def request(self, flow: HTTPFlow):
        pass

    def response(self, flow: HTTPFlow):
        pass

    def done(self):
        pass


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
