FROM python:3.13-slim
RUN pip install --no-cache-dir radicale passlib
RUN mkdir -p /var/lib/radicale/collections /etc/radicale
COPY config /etc/radicale/config
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
VOLUME ["/var/lib/radicale"]
EXPOSE 8080
ENTRYPOINT ["/entrypoint.sh"]