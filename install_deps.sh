#!/bin/bash
apt-get update
apt-get --assume-yes install python3-pip
apt-get --assume-yes install minisat
pip3 install bidict
pip3 install numpy
pip3 install networkx
pip3 install satispy
pip3 install toposort