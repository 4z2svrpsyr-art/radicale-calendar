#!/bin/sh
set -e

# Create default user from env vars
USER="${RADICALE_USER:-johnathan}"
PASS="${RADICALE_PASS:-changeme}"

python3 -c "
from passlib.hash import bcrypt
import os
h = bcrypt.hash(os.environ.get('RADICALE_PASS', 'changeme'))
with open('/etc/radicale/users', 'w') as f:
    f.write(f\"${os.environ.get('RADICALE_USER', 'johnathan')}:{h}\n\")
print(f'User ${os.environ.get(\"RADICALE_USER\", \"johnathan\")} created')
"

exec radicale --config /etc/radicale/config
