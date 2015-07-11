#!/bin/bash

# Postgres
apt-get -y -q install postgresql-9.3
apt-get -y -q install postgresql-client-9.3
apt-get -y -q install postgresql-contrib-9.3
apt-get -y -q install libpq-dev

# http://jacobian.org/writing/pg-encoding-ubuntu/
sudo -u postgres pg_dropcluster --stop 9.3 main
sudo -u postgres pg_createcluster --start -e UTF-8 9.3 main

# Configuração para psql permitir dump
cp pg_hba.conf /etc/postgresql/9.3/main/pg_hba.conf
service postgresql restart
