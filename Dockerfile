FROM python:3.12-slim

WORKDIR /app
COPY scripts/read_config.py /app/read_config.py
COPY config.yaml /app/config.yaml


RUN pip install --no-cache-dir pyyaml pillow numpy


CMD ["python", "/app/read_config.py"]

