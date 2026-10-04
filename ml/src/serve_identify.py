"""LAN identify API. Flutter POSTs a photo; this process runs the Colab SVM.

    python ml/src/serve_identify.py
    adb reverse tcp:8765 tcp:8765
"""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

try:
    from .identify import identify_bytes, load_model
except ImportError:
    from identify import identify_bytes, load_model

MAX_BYTES = 8 * 1024 * 1024
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8765

_MODEL = None


def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = load_model()
    return _MODEL


def identify_payload(body: bytes) -> tuple[int, dict]:
    if not body:
        return 400, {"success": False, "error": {"message": "Empty image body."}}
    if len(body) > MAX_BYTES:
        return 413, {"success": False, "error": {"message": "Image is too large."}}
    try:
        result = identify_bytes(body, model=get_model())
    except Exception as exc:
        return 400, {
            "success": False,
            "error": {"message": f"Could not read image ({type(exc).__name__})."},
        }
    return 200, {
        "success": True,
        "data": {
            "slug": result["slug"],
            "confidence": result["confidence"],
            "low_confidence": result["low_confidence"],
            "top": result["top"],
        },
    }


class IdentifyHandler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload: dict) -> None:
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Accept")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        if self.path.rstrip("/") == "/api/v1/health":
            self._send(200, {"success": True, "data": {"ok": True, "model": "svm_v1"}})
            return
        self._send(404, {"success": False, "error": {"message": "Not found."}})

    def do_POST(self) -> None:  # noqa: N802
        if self.path.rstrip("/") != "/api/v1/identify":
            self._send(404, {"success": False, "error": {"message": "Not found."}})
            return
        length = int(self.headers.get("Content-Length") or "0")
        body = self.rfile.read(length) if length else b""
        status, payload = identify_payload(body)
        self._send(status, payload)

    def log_message(self, format: str, *args) -> None:
        print("%s - %s" % (self.address_string(), format % args), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="MarineSee SVM identify server.")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    get_model()
    server = ThreadingHTTPServer((args.host, args.port), IdentifyHandler)
    print(f"identify API http://127.0.0.1:{args.port}/api/v1/identify", flush=True)
    print("phone USB: adb reverse tcp:{0} tcp:{0}".format(args.port), flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
