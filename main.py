import asyncio
import json
import time
import csv
import keyring
import sys
from interface import deribit_interface
from load_credentials import CLIENT_ID, CLIENT_SECRET

if CLIENT_ID == '' or CLIENT_SECRET == '':
	sys.exit('Run save_credentials.py first in order to store your credentials on this machine!')

### system value ###
deribit = deribit_interface.Deribit(test=False,
	client_ID=CLIENT_ID,
 	client_secret=CLIENT_SECRET)
logwritter = deribit.logwritter

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
			all_instruments.append(book['result']['instrument_name'])
		return all_instruments
	except Exception as e:
		print('Error in create_instruments: ', e)

def extract_greeks(instrument, ob):
	return [instrument, ob['greeks']]

def save_dict_to_file(dic):
	# Todo: This must be appended for each dictionary to come
    f = open('dict.txt','a')
    f.write(str(dic) + '\n')
    f.close()

def check_memory(_list, max_len = 1000):
	if len(_list) > max_len:
		_list = []
	return _list


all_option_instruments = create_instruments('BTC', 'option')

pausetime = 5
collected_trades = []
while True:
	# All orderbooks
	for instrument in all_option_instruments:
		ob = deribit.get_order_book(instrument)
		if ob is not None:
			print(instrument)
			print(ob)
			save_dict_to_file(extract_greeks(instrument, ob))
		time.sleep(pausetime)

	# All executed trades
	trades = deribit.get_last_trades_by_currency('BTC', 'option', 30) # TO BE DONE
	if trades is not None:
		for trade in trades['trades']:
			if trade not in collected_trades:
				collected_trades.append(trade)
				save_dict_to_file(trade)
	check_memory(trades)
	time.sleep(pausetime)

