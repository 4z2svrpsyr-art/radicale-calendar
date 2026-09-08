#!/bin/sh
set -e
echo ">>> Creating user ${RADICALE_USER:-johnathan}..."
echo "${RADICALE_USER:-johnathan}:${RADICALE_PASS:-changeme}" > /etc/radicale/users
echo ">>> User file: $(cat /etc/radicale/users)"
echo ">>> Config port: $(grep hosts /etc/radicale/config)"
echo ">>> Starting Radicale..."
exec radicale --config /etc/radicale/config --debug 2>&1