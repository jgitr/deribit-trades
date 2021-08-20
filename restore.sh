# Restore ETH data on BRC Server
# Target Command: mongorestore -d deribit-eth --gzip deribit-eth

PTH="/home/julian/imported_from_g2"
LATEST_UPLOAD=$(ls -td $PTH/*/ | head -1)
DBNAME="deribit-eth"

echo $LATEST_UPLOAD

mongorestore -d $DBNAME --gzip $LATEST_UPLOAD/$DBNAME