FROM alpine:latest

RUN apk add --no-cache \
    tcpdump \
    python3 \
    py3-pip \
    bash

COPY icmp_receiver.py /root/
COPY start_listener.sh /root/

RUN chmod +x /root/start_listener.sh

WORKDIR /root

RUN echo 'export PS1="\[\033[0;33m\]exfilserver@\h:\w\$ \[\033[0m\]"' >> /root/.bashrc

CMD ["/root/start_listener.sh"]
