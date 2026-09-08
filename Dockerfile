FROM python:3.13-slim

RUN pip install radicale radicale-auth-bcrypt passlib bcrypt

RUN mkdir -p /var/lib/radicale/collections /etc/radicale
COPY config /etc/radicale/config
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

VOLUME ["/var/lib/radicale"]
EXPOSE 5232

ENTRYPOINT ["/entrypoint.sh"]
