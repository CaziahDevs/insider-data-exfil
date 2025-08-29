FROM kalilinux/kali-rolling

RUN apt-get update && apt-get install -y \
    ettercap-text-only \
    netcat-traditional \
    iputils-ping \
    tcpdump \
    python3 \
    python3-pip \
    python3-scapy \
    mariadb-client \
    --no-install-recommends \
    && apt-get clean

WORKDIR /root/attacker

# Copy attack scripts
COPY scripts/ /root/attacker/

# Make scripts executable
RUN chmod +x /root/attacker/*.sh
RUN chmod +x /root/attacker/*.py

CMD ["tail", "-f", "/dev/null"]
