FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    tcpdump \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir scapy

COPY icmp_receiver.py /root/

RUN chmod +x /root/icmp_receiver.py

WORKDIR /root

RUN echo 'export PS1="\[\033[0;33m\]exfilserver@\h:\w\$ \[\033[0m\]"' >> /root/.bashrc

CMD ["tail", "-f", "/dev/null"]
