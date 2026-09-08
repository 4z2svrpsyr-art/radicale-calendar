#!/bin/sh
set -e
python3 -c "
from passlib.hash import sha256_crypt
import os
h = sha256_crypt.hash(os.environ.get(\"RADICALE_PASS\", \"changeme\"))
with open(\"/etc/radicale/users\", \"w\") as f:
    f.write(f\"${os.environ.get(\"RADICALE_USER\", \"johnathan\")}:{h}\n\")
print(\"User created\")
"
exec radicale --config /etc/radicale/config