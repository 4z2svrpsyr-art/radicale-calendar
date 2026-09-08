#!/bin/sh
set -e
echo "${RADICALE_USER:-johnathan}:${RADICALE_PASS:-changeme}" > /etc/radicale/users
echo ">>> User created"
echo ">>> Starting Radicale on :5232"
exec radicale --config /etc/radicale/config