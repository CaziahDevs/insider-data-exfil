FROM kalilinux/kali-rolling

RUN apt-get update && apt-get install -y \
    ettercap-text-only \
    netcat-traditional \
    iputils-ping \
    tcpdump \
    net-tools \
    iproute2 \
    python3 \
    python3-pip \
    python3-scapy \
    mariadb-client \
    --no-install-recommends \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /root/attacker

# Copy attack scripts
COPY scripts/ /root/attacker/

# Make scripts executable
RUN chmod +x /root/attacker/*.sh \
 && chmod +x /root/attacker/*.py

# Disable IPv6 so Ettercap doesn’t complain
RUN echo "net.ipv6.conf.all.disable_ipv6 = 1" >> /etc/sysctl.conf


CMD ["tail", "-f", "/dev/null"]
