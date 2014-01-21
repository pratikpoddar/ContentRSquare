#!/bin/bash

source /home/ubuntu/crsq-virtualenv/bin/activate
now=$(date +"%D %T")
echo "Current time: $now"
python /home/ubuntu/crsq/manage.py runcrons

