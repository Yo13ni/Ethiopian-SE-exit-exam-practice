import json
from http.server import BaseHTTPRequestHandler

from _backend import load_catalog, load_deep


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        catalog = load_catalog()
        deep_counts = {e["id"]: len(load_deep(e["id"])) for e in catalog.get("exams", [])}
        body = json.dumps(
            {
                "ok": True,
                "exams": catalog.get("exams", []),
                "deepCounts": deep_counts,
            }
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
