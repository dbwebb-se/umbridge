#!/bin/bash
TIME=`date +%H-%b-%d-%y`                       # This Command will read the date.                       
FILENAME="backup-db-$TIME.tar.gz"             # The filename including the date.                        
SRCDIR="/home/deploy/umbridge/app.db"         # Source backup folder.                                   
DESDIR="/home/deploy/db_backup"                              # Destination of backup file.              
tar -cPpzf $DESDIR/$FILENAME $SRCDIR
rsync -avz -e "ssh -i /home/deploy/.ssh/dbwebb" "$DESDIR/$FILENAME" umbridge@ssh.student.bth.se:db_backup/
rm "$DESDIR/$FILENAME"

# Add to crontab on umbridge
# 0 3 */1 * * sh /home/deploy/umbridge/backup_db.sh

# Add to crontab on studentserver
# 14 * * * find /<path-to-user>/db_backup/* -maxdepth 0 -mtime +7  | xargs rm -rf >/dev/null 2>&1
