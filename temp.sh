#!/bin/sh

set -ex

apt-get install -y python3-statsd

cd $(dirname "$0")
install temp.py /usr/local/bin
install temp.service /etc/systemd/system
systemctl enable temp
systemctl start temp
