#!/bin/bash
apt-get update
apt-get --assume-yes install python3-pip
pip3 install bidict
pip3 install numpy
pip3 install networkx
pip3 install satispy
pip3 install toposort


rm -rf lib/*
mkdir -p lib
wget -O lib/fastjson-1.2.45.jar http://search.maven.org/remotecontent?filepath=com/alibaba/fastjson/1.2.45/fastjson-1.2.45.jar

