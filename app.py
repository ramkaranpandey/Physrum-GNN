"""Offline dynamic Guwahati routing lab: python app.py."""
import json
import os
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from physrum.dynamic import GRAPH, DEFAULT_START, DEFAULT_END, DISPLAY_BOUNDS
from physrum.fleet import Fleet, DEPOTS, ZONES, MAX_PAIRS, default_pairs
from physrum.graph import RoadGraph

ROOT=Path(__file__).resolve().parent
HTML=(ROOT/'fleet.html').read_bytes()
ALLOWED_ORIGINS={origin.strip() for origin in os.environ.get('CORS_ALLOWED_ORIGINS','*').split(',') if origin.strip()}
SESSIONS={}
BACKGROUND=RoadGraph(bounds=DISPLAY_BOUNDS)
BACKGROUND.edges.extend(edge for edge in GRAPH.edges if edge.get('simulated'))
DEFAULT_PAIRS=default_pairs()

class Handler(BaseHTTPRequestHandler):
    def cors_headers(self):
        origin=self.headers.get('Origin')
        if '*' in ALLOWED_ORIGINS:
            self.send_header('Access-Control-Allow-Origin','*')
        elif origin in ALLOWED_ORIGINS:
            self.send_header('Access-Control-Allow-Origin',origin)
            self.send_header('Vary','Origin')
        self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.send_header('Access-Control-Max-Age','86400')
    def respond(self,value,status=200):
        data=json.dumps(value).encode('utf8')
        self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store')
        self.cors_headers()
        self.end_headers();self.wfile.write(data)
    def do_OPTIONS(self):
        self.send_response(204)
        self.cors_headers()
        self.send_header('Content-Length','0')
        self.end_headers()
    def do_GET(self):
        path=urlsplit(self.path).path
        if path=='/healthz':
            return self.respond({'status':'ok','service':'physrum-fleet-api'})
        if path=='/config.js':
            config=(ROOT/'config.js').read_bytes()
            self.send_response(200);self.send_header('Content-Type','application/javascript; charset=utf-8')
            self.send_header('Content-Length',str(len(config)));self.send_header('Cache-Control','no-store')
            self.end_headers();self.wfile.write(config)
        elif path=='/':
            self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Cache-Control','no-store')
            self.send_header('Content-Length',str(len(HTML)));self.end_headers();self.wfile.write(HTML)
        elif path=='/api/map':
            self.respond({'nodes':GRAPH.nodes,'edges':BACKGROUND.edges,
                'background_nodes':BACKGROUND.nodes,
                'default_start':DEFAULT_START,'default_end':DEFAULT_END,
                'depots':DEPOTS,'zones':ZONES,
                'default_pairs':DEFAULT_PAIRS,'max_pairs':MAX_PAIRS,
                'title':'Maligaon-Kamakhya · OSM-derived road close-up'})
        elif path.startswith('/api/state/'):
            session=SESSIONS.get(path.split('/')[-1])
            if session:self.respond(session.get())
            else:self.respond({'error':'Simulation not found'},404)
        else:self.respond({'error':'Not found'},404)
    def do_POST(self):
        if urlsplit(self.path).path!='/api/start':return self.respond({'error':'Not found'},404)
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<10000:raise ValueError('Invalid request size.')
            body=json.loads(self.rfile.read(size))
            pairs=body.get('pairs')
            if pairs is not None and not isinstance(pairs,list):
                raise ValueError('pairs must be a list of [start, end] items.')
            session=Fleet(count=int(body.get('count',50)),
                          start=body.get('start',DEFAULT_START),
                          target=body.get('target',DEFAULT_END),
                          seed=int(body.get('seed',2306)),
                          pairs=pairs)
            key=uuid.uuid4().hex
            SESSIONS[key]=session
            threading.Thread(target=session.run,daemon=True).start()
            self.respond({'session':key,'initial':session.initial,
                          'depots':session.depots,'zones':session.zones,
                          'pairs':session.pairs})
        except (ValueError,TypeError,KeyError,json.JSONDecodeError) as exc:
            self.respond({'error':str(exc)},400)

def main():
    # Render supplies PORT; local runs default to port 8000.
    host=os.environ.get('HOST','0.0.0.0')
    port=int(os.environ.get('PORT','8000'))
    server=ThreadingHTTPServer((host,port),Handler)
    print(f'PHYSRUM Fleet API listening on {host}:{port}',flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__=='__main__':main()
