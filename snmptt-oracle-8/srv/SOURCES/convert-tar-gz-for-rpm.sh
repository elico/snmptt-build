#!/usr/bin/env sh

wget https://github.com/snmptt/snmptt/archive/refs/tags/snmptt_1-5.tar.gz -O snmptt_1-5.tar.gz
tar xvf snmptt_1-5.tar.gz
mkdir snmptt_1.5
mv -v snmptt-snmptt_*/snmptt/* snmptt_1.5/
tar cvfz snmptt_1.5.tar.gz snmptt_1.5

rm -rf snmptt-snmptt_1-5/
rm -rf snmptt_1.5/
