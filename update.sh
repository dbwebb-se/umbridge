#!/bin/sh

##
# Script to update and restart umbridge with the latest code.
# Repo needs to be public.
##

HOST="umbridge.arnesson.dev"
SSH_USER="deploy"
SSH_KEY_LOCATION="~/.ssh/umbridge.pem"
COMMAND="cd ~/umbridge; git pull --rebase; sudo cp /var/log/supervisor/*.log /home/$SSH_USER/log_backup/; sudo supervisorctl reload"

ssh -i ${SSH_KEY_LOCATION} ${SSH_USER}@${HOST} "${COMMAND}"