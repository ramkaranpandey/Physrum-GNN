"""Offline interactive demo: python app.py (Python standard library only)."""
import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from physrum.experiment import SCENARIOS, load, route_setup, run_one

ROOT = Path(__file__).resolve().parent
HTML = (ROOT / "dashboard.html").read_bytes()


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, content, mime="application/json; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def data(self, value, status=200):
        self.reply(status, json.dumps(value).encode("utf-8"))

    def do_GET(self):
        url = urlsplit(self.path)
        if url.path == "/":
            return self.reply(200, HTML, "text/html; charset=utf-8")
        if url.path == "/api/scenario":
            key = parse_qs(url.query).get("name", ["maligaon"])[0]
            if key not in SCENARIOS:
                return self.data({"error": "Unknown scenario"}, 400)
            graph, start, target, original = route_setup(key)
            return self.data({"name": key, "title": SCENARIOS[key]["name"],
                "hazard": SCENARIOS[key]["kind"],
                "edges": [[e["id"], e["geometry"], e["oneway"]] for e in graph.edges],
                "original": original, "start": graph.nodes[start], "target": graph.nodes[target]})
        self.data({"error": "Page not found"}, 404)

    def do_POST(self):
        if self.path != "/api/run":
            return self.data({"error": "Page not found"}, 404)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length < 10000:
                raise ValueError("Request size is invalid")
            body = json.loads(self.rfile.read(length))
            key = body.get("scenario")
            if key not in SCENARIOS:
                raise ValueError("Select a valid scenario")
            ids = body.get("closed", [])
            if not isinstance(ids, list) or len(ids) > 30 or any(type(i) is not int or i < 0 for i in ids):
                raise ValueError("Enter up to 30 numeric road IDs")
            if ids:
                manual = set(ids)
            else:
                manual = None  # choose the scenario's recoverable default closure
            rows, evaluation, path = run_one(key, SCENARIOS[key], load(), manual=manual)
            result = json.loads(path.read_text(encoding="utf-8"))
            result["evaluation"] = evaluation
            self.data(result)
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            self.data({"error": str(exc)}, 400)
        except Exception:
            self.log_exception()
            self.data({"error": "Simulation failed; check the server console"}, 500)

    def log_exception(self):
        import traceback
        traceback.print_exc()


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    print("PHYSRUM-GNN dashboard: http://127.0.0.1:8765", flush=True)
    print("Keep this window open; press Ctrl+C to stop.", flush=True)
    threading.Timer(0.8, lambda: webbrowser.open("http://127.0.0.1:8765")).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


if __name__ == "__main__":
    main()
