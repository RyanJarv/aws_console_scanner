import http
import json
import logging
import os
import sys
from threading import Thread
from queue import Queue
from typing import TextIO

from mitmproxy import ctx
from mitmproxy.addonmanager import Loader
from mitmproxy.http import HTTPFlow
from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster


class Addon(object):
    def __init__(self):
        self.queue = Queue()
        self.output: TextIO = None

    def load(self, loader: Loader):
        loader.add_option('json_output_file', str, 'output/dump.json', 'Output destination: path to a file or URL.')

    def configure(self, _):
        dest_dir = os.path.dirname(os.path.join(os.getcwd(), ctx.options.json_output_file))
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        self.output = open(ctx.options.json_output_file, 'a')

        t = Thread(target=self.worker)
        t.start()

    def request(self, flow: HTTPFlow):
        pass

    def response(self, flow: HTTPFlow):
        self.queue.put(flow.copy())

    def worker(self):
        while True:
            try:
                frame = self.queue.get()
                self.dump(frame)
                self.queue.task_done()
            except Exception as e:
                logging.exception("[ERROR]")

    def dump(self, flow: HTTPFlow):
        host = flow.request.host
        if not ('aws' in host or 'amazon' in host):
            return

        hdrs = flow.response.headers
        resp_content_type = hdrs.get('Content-Type')
        if not resp_content_type:
            return
        elif 'json' not in resp_content_type:
            return

        try:
            flow_data = {
                "req.content_type": hdrs.get('Content-Type'),
                "req.host": flow.request.host,
                "req.path": flow.request.path,
                "req.content": flow.request.content,
                "resp.content_type": hdrs.get('Content-Type'),
                "resp.status_code": flow.response.status_code,
                "resp.content": flow.response.content,
            }
        except UnicodeDecodeError as e:
            print("[WARN] {}".format(str(e)))
            return

        self.output.write(json.dumps(flow_data, default=decode_bytes))
        self.output.flush()

    def done(self):
        self.output.close()


def decode_bytes(b: bytes):
    try:
        return b.decode()
    except Exception as e:
        return TypeError(e)


class ProxyMaster(DumpMaster):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, **kwargs):
        try:
            DumpMaster.run(self, **kwargs)
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
        cert_passphrase=paswd,
    )
    config = ProxyConfig(options)
    master = ProxyMaster(options, with_termlog=True, with_dumper=True)
    master.addons.add(Addon())
    master.server = ProxyServer(config)
    master.options.update(json_output_file='output/dump.json')
    master.run()
