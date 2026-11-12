"""Offline fictional-city routing lab: python app.py."""
import json
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from physrum.graph import RoadGraph
from physrum.physarum import adapt

ROOT=Path(__file__).resolve().parent
CITY=ROOT/'data'/'custom_city.json'
HTML=(ROOT/'city.html').read_bytes()
GRAPH=RoadGraph(CITY)
META=json.loads(CITY.read_text(encoding='utf8'))['meta']

def solve(start,target,closed,method):
    if start not in GRAPH.nodes or target not in GRAPH.nodes or start==target:
        raise ValueError('Choose two different intersections on the city map.')
    if len(closed)>30 or any(type(i) is not int or i not in GRAPH.by_id for i in closed):
        raise ValueError('Choose up to 30 valid road segments.')
    blocked=set(closed)
    original=GRAPH.dijkstra(start,target)
    if original is None:raise ValueError('No original route exists for those intersections.')
    if method=='physarum':
        _,warm,pressure=adapt(GRAPH,start,target,set(),rounds=4)
        tic=time.perf_counter_ns()
        route,_,_=adapt(GRAPH,start,target,blocked,warm,prior_pressure=pressure)
    elif method=='dijkstra':
        tic=time.perf_counter_ns()
        route=GRAPH.dijkstra(start,target,blocked)
    else:raise ValueError('Unknown method.')
    ms=(time.perf_counter_ns()-tic)/1e6
    valid=GRAPH.valid(route,start,target,blocked)
    return {'method':method,'original':original,'original_valid':GRAPH.valid(original,start,target,blocked),
            'route':route,'valid':valid,'drive_min':round(GRAPH.drive_time(route),3) if valid else None,
            'reroute_ms':round(ms,3),'blocked':sorted(blocked),
            'pre_event_drive_min':round(GRAPH.drive_time(original),3)}

class Handler(BaseHTTPRequestHandler):
    def respond(self,value,status=200):
        data=json.dumps(value).encode('utf8')
        self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store')
        self.end_headers();self.wfile.write(data)
    def do_GET(self):
        if self.path=='/':
            self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Content-Length',str(len(HTML)));self.end_headers();self.wfile.write(HTML)
        elif self.path=='/api/city':
            self.respond({'meta':META,'nodes':GRAPH.nodes,'edges':GRAPH.edges})
        else:self.respond({'error':'Not found'},404)
    def do_POST(self):
        if self.path!='/api/route':return self.respond({'error':'Not found'},404)
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<10000:raise ValueError('Invalid request size.')
            body=json.loads(self.rfile.read(size))
            closed=body.get('closed',[])
            if not isinstance(closed,list):raise ValueError('Blocked road IDs must be a list.')
            self.respond(solve(body.get('start'),body.get('target'),closed,body.get('method')))
        except (ValueError,TypeError,KeyError,json.JSONDecodeError) as exc:
            self.respond({'error':str(exc)},400)

def main():
    server=ThreadingHTTPServer(('127.0.0.1',8765),Handler)
    print('Aster City routing lab: http://127.0.0.1:8765',flush=True)
    print('Keep this window open; Ctrl+C to stop.',flush=True)
    threading.Timer(.8,lambda:webbrowser.open('http://127.0.0.1:8765')).start()
    try:server.serve_forever()
    except KeyboardInterrupt:server.server_close()

if __name__=='__main__':main()
