#!/bin/bash -xe
 
# clean out all caches
yum clean all

yum install -y epel-release

yum install -y deltarpm python-deltarpm

yum update -y "*lib*"

# Needed to fix git clone
yum update -y nss curl libcurl
