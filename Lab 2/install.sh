#!/bin/bash

apt-get update
apt-get install python3 python3-dev python3-pip git
pip3 install --upgrade git+https://github.com/arthaud/python3-pwntools.git
