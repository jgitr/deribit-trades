import asyncio
import json
import time
import csv
import keyring
import sys
from interface import deribit_interface
from load_credentials import CLIENT_ID, CLIENT_SECRET
from pymongo import MongoClient
from mails import send_mail
from datetime import datetime 

if CLIENT_ID == '' or CLIENT_SECRET == '':
	sys.exit('Run save_credentials.py first in order to store your credentials on this machine!')

### system value ###
deribit = deribit_interface.Deribit(test=False,
	client_ID=CLIENT_ID,
 	client_secret=CLIENT_SECRET)
logwriter = deribit.logwriter

def create_instruments(_currency, _kind):
	# Get all instruments from a request
	try:
		all_instruments = []
		book_summaries = deribit.get_book_summary_by_currency(_currency, _kind)
		for book in book_summaries:
			all_instruments.append(book['instrument_name'])
		return all_instruments
	except Exception as e:
		print('Error in create_instruments: ', e)

def extract_greeks(instrument, ob):
	return [instrument, ob['greeks']]

def save_dict_to_file(dict, fname):
	# Todo: This must be appended for each dictionary to come
    f = open(fname + '.txt','a')
    f.write(str(dict) + '\n')
    f.close()

def check_memory(_list, max_len = 3000):
	curr_len = len(_list)
	if curr_len > max_len:
		del _list[:max_len]
	return _list

def main(base_currencies):

	"""
	Should rather use while true loop
	iterate over BTC, ETH, SOL

	"""

	# Track retrieved trades across the iterations
	orderbook_file 			= 'orderbooks'
	trade_file 				= 'trades'
	collected_change_ids 	= []
	collected_trades 		= []
	
	while True:

		starttime = datetime.now()
		
		for base_currency in base_currencies:
			
			client = MongoClient('mongodb://localhost:27017')
			dbname = str('DERIBIT-') + base_currency
			db = client[dbname]
			orderbooks = db.orderbooks
			transactions = db.transactions

			try:
			# Retrieve all instruments
				all_option_instruments = create_instruments(base_currency, 'option')
				assert(len(all_option_instruments) > 0)

				# All executed trades
				trades = deribit.get_last_trades_by_currency(base_currency, 'option', 100) # TO BE DONE
				if trades is not None:
					for trade in trades['trades']:
						if trade not in collected_trades:
							collected_trades.append(trade)

							# Add to db
							res_transactions = transactions.insert_one(trade)
							print('One trade: {0}'.format(res_transactions.inserted_id))


				
				time.sleep(1)
				# All orderbooks
				for instrument in all_option_instruments:
					ob = deribit.get_order_book(instrument)
					if ob is not None:
						print(instrument)
						print(ob)
						if ob['change_id'] not in collected_change_ids:
							collected_change_ids.append(ob['change_id'])

							# Add to db
							res = orderbooks.insert_one(ob)
							print('One orderbook: {0}'.format(res.inserted_id))

							# For the Rate Limit
							time.sleep(0.15)

						else:
							print('already got orderbook')
				
				
				check_memory(collected_change_ids)

			except Exception as e:
				logwriter('Error ', e)
				send_mail(e, 'Error in: ' + base_currency)
				time.sleep(1)
			finally:
				endtime = datetime.now()
				print('Runtime: ', endtime - starttime)
				time.sleep(1)

if __name__ == '__main__':
	main(base_currencies = ['BTC', 'ETH', 'SOL'])
			
