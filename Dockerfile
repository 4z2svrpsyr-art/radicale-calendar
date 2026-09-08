FROM python:3.13-alpine
RUN mkdir -p /data
COPY server.py /server.py
EXPOSE 80
CMD ["python3", "/server.py"]