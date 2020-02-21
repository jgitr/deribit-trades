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
	call = 'BTC-' + maturitystr + '-' + str(strike) + '-C'
	put = 'BTC-' + maturitystr + '-'+ str(strike) + '-P'
	return call, put


all_maturitystr = ['28FEB20']
all_strikes = [10000, 10250]
all_instruments = []

for maturity in all_maturitystr:
	for k in all_strikes:
		call, put = construct_instruments(maturity, k)
		all_instruments.append(call)
		all_instruments.append(put)
print(all_instruments)

# Retrieving trades works now // example
#trades = deribit.get_last_trades_by_currency('BTC', 'option', 30) # TO BE DONE
#print(trades)

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

pausetime = 5
collected_trades = []
while True:
		trades = deribit.get_last_trades_by_currency('BTC', 'option', 30) # TO BE DONE
		if trades is not None:
			for trade in trades['trades']:
				if trade not in collected_trades and trade['instrument_name'].startswith('BTC-28FEB20'):
					collected_trades.append(trade)
					save_dict_to_file(trade)
		check_memory(trades)
		time.sleep(pausetime)

