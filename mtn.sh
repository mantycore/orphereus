#!/bin/bash

# Deprecated calls
#RND=`date | md5sum | awk '{print $1}'`
#echo -n $RND > /var/py/orphie/fc/secid
#wget --output-document=/tmp/lastMaintenance.html http://anoma.ch/holySynod/service/all/$RND

cd /opt/orphereus
paster maintenance --config=prod.ini --path=. RunAllObligatory > /tmp/orphereus.maintenanct.log 2>&1
