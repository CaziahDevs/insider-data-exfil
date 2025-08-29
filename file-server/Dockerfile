FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=AcmeDB2024!
ENV MYSQL_DATABASE=customer_db
ENV MYSQL_USER=sarah_chen
ENV MYSQL_PASSWORD=Portfolio2024!

# Copy initialization scripts and sample data
COPY init-scripts/ /docker-entrypoint-initdb.d/

# Enable query logging for the demonstration
COPY mysql-config.cnf /etc/mysql/conf.d/

#Shell color
RUN echo 'export PS1="\[\033[0;32m\]fileserver@\h:\w\$ \[\033[0m\]"' >> /root/.bashrc

EXPOSE 3306
