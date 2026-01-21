FROM python:3.12-slim

WORKDIR /app

# Pillow needs a few basic libs; this keeps it smooth on slim images
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-dejavu-core \
 && rm -rf /var/lib/apt/lists/*

COPY surreal_cathedral.py /app/surreal_cathedral.py

RUN pip install --no-cache-dir pillow

# By default, write outputs to /out (we'll mount this to your host)
CMD ["python", "/app/surreal_cathedral.py"]
