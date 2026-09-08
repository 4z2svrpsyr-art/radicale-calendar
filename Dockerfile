FROM x1unix/docker-radicale:latest
COPY config /etc/radicale/config
VOLUME ["/data"]
EXPOSE 5232