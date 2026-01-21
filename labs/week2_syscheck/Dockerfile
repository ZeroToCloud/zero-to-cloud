FROM ubuntu:24.04

RUN apt-get update && apt-get install -y --no-install-recommends \
  procps iproute2 util-linux coreutils docker.io curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY syscheck.sh /app/syscheck.sh
RUN chmod +x /app/syscheck.sh

CMD ["/app/syscheck.sh"]
