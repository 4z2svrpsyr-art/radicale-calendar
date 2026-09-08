#!/bin/sh
python3 -c "
import bcrypt, os
pw = os.environ.get(\"RADICALE_PASS\", \"changeme\")
user = os.environ.get(\"RADICALE_USER\", \"johnathan\")
with open(\"/data/users\", \"w\") as f:
    f.write(f\"{user}:{bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()}\n\")
print(\"User created\")
"
exec radicale --config /etc/radicale/config