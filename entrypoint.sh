#!/bin/sh
set -e
python3 -c "
import hashlib, os, base64
pw = os.environ.get(\"RADICALE_PASS\", \"changeme\")
user = os.environ.get(\"RADICALE_USER\", \"johnathan\")
salt = os.urandom(6).hex()
h = base64.b64encode(hashlib.sha256((pw + salt).encode()).digest()).decode()
with open(\"/etc/radicale/users\", \"w\") as f:
    f.write(f\"{user}:{h}\\n\")
print(\">>> User created\")
"
echo ">>> Starting Radicale on :5232"
exec radicale --config /etc/radicale/config