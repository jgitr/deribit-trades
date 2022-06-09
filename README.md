# Deribit Option Scraper
- Iterates over BTC, ETH, SOL contracts 
- Retrieves orderbooks and trades if they are unknown
- Stored in a MongoDB for each base currency

A cronjob restarts the Scraper frequently in case of hickups.
Automatic backups and syncs.

# Common Errors
- Cannot have similarly named databases
- Got to stick to the rate limit
