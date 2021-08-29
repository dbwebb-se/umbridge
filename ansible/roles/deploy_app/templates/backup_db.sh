#!/bin/bash
TIME=`date +%H-%b-%d-%y`                       # This Command will read the date.
FILENAME="backup-db-$TIME.tar.gz"             # The filename including the date.
SRCDIR="/home/{{ server_user }}/umbridge/app.db"         # Source backup folder.
DESDIR="/home/{{ server_user }}/db_backup"                              # Destination of backup file.
tar -cpzf $DESDIR/$FILENAME $SRCDIR
rsync -avz -e "ssh -i /home/{{ server_user }}/.ssh/dbwebb" "$DESDIR/$FILENAME" umbridge@ssh.student.bth.se:db_backup/
