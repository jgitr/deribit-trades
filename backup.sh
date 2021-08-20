#!/bin/sh

#=====================================================================
# Set the following variables as per your requirement
#=====================================================================
# Database Name to backup
MONGO_DATABASE="deribit-eth"
# Database host name
MONGO_HOST="127.0.0.1"
# Database port
MONGO_PORT="27017"
# Backup directory
BACKUPS_DIR="/Users/julian/src/deribit-trades/backups/$MONGO_DATABASE"
# Database user name
DBUSERNAME="username"
# Database password
DBPASSWORD="passw0rd"
# Authentication database name
DBAUTHDB="admin"
# Days to keep the backup
DAYSTORETAINBACKUP="14"
# BRC Import Path
brc_path="/home/julian/imported_from_g2"
#=====================================================================

TIMESTAMP=`date +%F-%H%M`
BACKUP_NAME="$MONGO_DATABASE-$TIMESTAMP"

echo "Performing backup of $MONGO_DATABASE"
echo "--------------------------------------------"
# Create backup directory
if ! mkdir -p $BACKUPS_DIR; then
  echo "Can't create backup directory in $BACKUPS_DIR. Go and fix it!" 1>&2
  exit 1;
fi;
# Create dump
mongodump -d $MONGO_DATABASE --gzip #--username $DBUSERNAME --password $DBPASSWORD --authenticationDatabase $DBAUTHDB
# Rename dump directory to backup name
mv dump $BACKUPS_DIR/$BACKUP_NAME
# Compress backup
#tar -zcvf $BACKUPS_DIR/$BACKUP_NAME.tgz $BACKUP_NAME
# Delete uncompressed backup
#rm -rf $BACKUP_NAME
# Delete backups older than retention period
find $BACKUPS_DIR -type f -mtime +$DAYSTORETAINBACKUP -exec rm {} +
echo "--------------------------------------------"
echo "Database backup complete!"

# Find latest dir for upload
UPLOADDIR=$(ls -td $BACKUPS_DIR/*/ | head -1)
echo $UPLOADDIR

# Upload to Server
echo "Attempting to upload to BRC Server"
scp -r $UPLOADDIR irtggmail:$brc_path/
echo "Upload successful"