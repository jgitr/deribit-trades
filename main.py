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

if CLIENT_ID == '' or CLIENT_SECRET == '':
	sys.exit('Run save_credentials.py first in order to store your credentials on this machine!')

### system value ###
deribit = deribit_interface.Deribit(test=False,
	client_ID=CLIENT_ID,
 	client_secret=CLIENT_SECRET)
logwriter = deribit.logwriter

def construct_instruments(maturitystr, strike):
	# Manually create instrument
	call = 'BTC-' + maturitystr + '-' + str(strike) + '-C'
	put = 'BTC-' + maturitystr + '-'+ str(strike) + '-P'
	return call, put


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

def check_memory(_list, max_len = 1000):
	curr_len = len(_list)
	if curr_len > max_len:
		del _list[:max_len]
	return _list


client = MongoClient('mongodb://localhost:27017')
db = client['pymongo_test']
orderbooks = db.orderbooks
transactions = db.transactions

orderbook_file 			= 'orderbooks'
trade_file 				= 'trades'
collected_change_ids 	= []
collected_trades 		= []
while True:
	try:
	# Retrieve all instruments
		all_option_instruments = create_instruments('BTC', 'option')
		assert(len(all_option_instruments) > 0)
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

				else:
					print('already got orderbook')
			check_memory(collected_change_ids)

		# All executed trades
		trades = deribit.get_last_trades_by_currency('BTC', 'option', 100) # TO BE DONE
		if trades is not None:
			for trade in trades['trades']:
				if trade not in collected_trades:
					collected_trades.append(trade)

					# Add to db
					res_transactions = transactions.insert_one(trade)
					print('One trade: {0}'.format(res_transactions.inserted_id))

			check_memory(trades)

	except Exception as e:
		logwriter('Error ', e)
		send_mail(e, 'Scraper Error')
		time.sleep(1)
	finally:
		time.sleep(1)


