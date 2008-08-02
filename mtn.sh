#!/bin/bash

RND=`date | md5sum | awk '{print $1}'`
echo -n $RND > /var/py/orphie/fc/secid
wget --output-document=/tmp/lastMaintenance.html http://anoma.ch/holySynod/service/all/$RND
