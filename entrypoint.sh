#!/bin/sh
set -e
echo "${RADICALE_USER:-johnathan}:${RADICALE_PASS:-changeme}" > /etc/radicale/users
echo "User created"
exec radicale --config /etc/radicale/config