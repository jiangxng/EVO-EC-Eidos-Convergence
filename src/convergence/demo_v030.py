from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .scenario_v030 import ApmLiveScenario

HTML = Path(__file__).with_name('demo_v030.html')


def run(host='127.0.0.1', port=8083, evo_url='http://127.0.0.1:3000'):
    from .evo_live_adapter import LiveEvoAdapter
    scenario = ApmLiveScenario(LiveEvoAdapter(base_url=evo_url))
    state = {'prepared': None}

    class Handler(BaseHTTPRequestHandler):
        def send_json(self, payload, status=200):
            data=json.dumps(payload,default=str).encode(); self.send_response(status)
            self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
        def do_GET(self):
            if self.path == '/':
                data=HTML.read_bytes(); self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data); return
            if self.path == '/api/state':
                self.send_json(state['prepared'] or {'status':'NOT_PREPARED'}); return
            self.send_error(404)
        def do_POST(self):
            try:
                if self.path == '/api/prepare':
                    state['prepared']=scenario.prepare_decision(); self.send_json(state['prepared']); return
                if self.path == '/api/approve':
                    if state['prepared'] is None: raise RuntimeError('Prepare decision first')
                    result=scenario.approve_and_execute(state['prepared']); state['prepared']={**state['prepared'],'result':result}; self.send_json(result); return
                self.send_error(404)
            except Exception as exc:
                self.send_json({'error':type(exc).__name__,'message':str(exc)},500)
        def log_message(self, fmt, *args):
            return

    print(f'APM v0.3 demo: http://{host}:{port}  EVO: {evo_url}')
    ThreadingHTTPServer((host,port),Handler).serve_forever()


if __name__ == '__main__':
    run()
