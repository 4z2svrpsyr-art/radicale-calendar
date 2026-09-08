import http.server, os, base64, sys

PORT = int(os.environ.get("PORT", 80))
USER = os.environ.get("RADICALE_USER", "johnathan")
PASS = os.environ.get("RADICALE_PASS", "changeme")
DATA_DIR = "/data"

class CalHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        auth = self.headers.get("Authorization", "")
        if auth.startswith("Basic "):
            creds = base64.b64decode(auth[6:]).decode().split(":", 1)
            if creds[0] == USER and creds[1] == PASS:
                return self.serve_cal()
        self.send_response(401)
        self.send_header("WWW-Authenticate", "Basic realm=\"Calendar\"")
        self.end_headers()

    def do_PUT(self):
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Basic "):
            return self.send_auth()
        creds = base64.b64decode(auth[6:]).decode().split(":", 1)
        if creds[0] != USER or creds[1] != PASS:
            return self.send_auth()
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        os.makedirs(DATA_DIR, exist_ok=True)
        path = os.path.join(DATA_DIR, self.path.lstrip("/") or "calendar.ics")
        with open(path, "wb") as f:
            f.write(body)
        self.send_response(201)
        self.end_headers()

    def send_auth(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", "Basic realm=\"Calendar\"")
        self.end_headers()
        self.wfile.write(b"Auth required")

    def serve_cal(self):
        path = self.path.lstrip("/") or "personal.ics"
        filepath = os.path.join(DATA_DIR, path)
        if os.path.exists(filepath):
            self.send_response(200)
            self.send_header("Content-Type", "text/calendar; charset=utf-8")
            self.send_header("Content-Disposition", f"attachment; filename=\"{path}\"")
            self.end_headers()
            with open(filepath, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/calendar; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"BEGIN:VCALENDAR\\nVERSION:2.0\\nPRODID:-//Hermes//Personal Calendar//EN\\nEND:VCALENDAR\\n")

if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", PORT), CalHandler)
    print(f"iCal server on :{PORT}")
    server.serve_forever()