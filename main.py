import asyncio
import json
import time
import csv
import keyring
import sys
from interface import deribit_interface

CLIENT_ID = ''
CLIENT_SECRET = ''

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


all_maturitystr = ['14FEB20', '28FEB20']
all_strikes = [10000, 10250]
all_instruments = []

for maturity in all_maturitystr:
	for k in all_strikes:
		call, put = construct_instruments(maturity, k)
		all_instruments.append(call)
		all_instruments.append(put)
print(all_instruments)

#trades = deribit.get_user_trades_by_instrument('ETH')
#trades = deribit.get_transactions('BTC', 10)
#trades = deribit.get_last_trades_by_currency('BTC', 'option') # TO BE DONE
#print(trades)

def extract_greeks(instrument, ob):
	return [instrument, ob['greeks']]

def save_dict_to_file(dic):
	# Todo: This must be appended for each dictionary to come
    f = open('dict.txt','a')
    f.write(str(dic) + '\n')
    f.close()

pausetime = 1
while True:
	for instrument in all_instruments:
		ob = deribit.get_order_book(instrument)
		if ob is not None:
			print(instrument)
			print(ob)
			save_dict_to_file(extract_greeks(instrument, ob))
		time.sleep(1)

