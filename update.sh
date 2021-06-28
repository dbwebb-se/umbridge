#!/bin/sh

##
# Script to update and restart umbridge with the latest code.
# Repo needs to be public.
##

HOST="40.87.149.99"
SSH_USER="azureuser"
SSH_KEY_LOCATION="/home/mabn17/.ssh/flask.pem"
COMMAND="cd ~/git/umbridge; git pull --rebase; sudo supervisorctl stop umbridge; sudo supervisorctl start umbridge"

ssh -i ${SSH_KEY_LOCATION} ${SSH_USER}@${HOST}