import http.server, os, base64, sys

PORT = int(os.environ.get("PORT", 80))
USER = os.environ.get("RADICALE_USER", "johnathan")
PASS = os.environ.get("RADICALE_PASS", "changeme")
DATA_DIR = "/data"

EMPTY_CAL = b"BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Hermes//Personal Calendar//EN\r\nX-WR-CALNAME:Personal\r\nEND:VCALENDAR\r\n"

class CalHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _check_auth(self):
        auth = self.headers.get("Authorization", "")
        if auth.startswith("Basic "):
            try:
                creds = base64.b64decode(auth[6:]).decode().split(":", 1)
                return creds[0] == USER and creds[1] == PASS
            except: pass
        return False

    def _send_auth(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", "Basic realm=\"Calendar\"")
        self.end_headers()
        self.wfile.write(b"Auth required")

    def do_GET(self):
        if not self._check_auth():
            return self._send_auth()
        path = self.path.lstrip("/") or "personal.ics"
        filepath = os.path.join(DATA_DIR, path)
        if ".." in path or not os.path.realpath(filepath).startswith(os.path.realpath(DATA_DIR)):
            self.send_response(403); self.end_headers(); return

        self.send_response(200)
        self.send_header("Content-Type", "text/calendar; charset=utf-8")
        self.end_headers()
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.wfile.write(EMPTY_CAL)

    def do_PUT(self):
        if not self._check_auth():
            return self._send_auth()
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        path = self.path.lstrip("/") or "personal.ics"
        filepath = os.path.join(DATA_DIR, path)
        if ".." in path or not os.path.realpath(filepath).startswith(os.path.realpath(DATA_DIR)):
            self.send_response(403); self.end_headers(); return
        with open(filepath, "wb") as f:
            f.write(body)
        self.send_response(201)
        self.end_headers()

if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", PORT), CalHandler)
    print(f"iCal server on :{PORT}")
    server.serve_forever()