#!/bin/bash -xe

#pip install --upgrade pip

# this also removes opencv-python
#yum erase -y numpy

#pip install --upgrade numpy
#pip install --upgrade opencv-python

cd /root
git clone https://github.com/slipstream/nuvlabox-video.git

#systemctl disable firewalld || true
#systemctl enable iptables
#iptables -t mangle -I OUTPUT -p tcp --sport 5000 -j DSCP --set-dscp-class EF
#service iptables save

