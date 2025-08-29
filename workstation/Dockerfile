FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    mysql-client \
    iputils-ping \
    net-tools \
    && apt-get clean

# Simulate employee behavior - periodic database queries
COPY db_queries.sh /home/workstation/
RUN chmod +x /home/workstation/db_queries.sh

# Shell color
RUN echo 'export PS1="\[\033[0;34m\]workstation@\h:\w\$ \[\033[0m\]"' >> /root/.bashrc

CMD ["tail", "-f", "/dev/null"]
