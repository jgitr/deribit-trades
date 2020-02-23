from websocket import create_connection
import websocket
from datetime import datetime
import json
import threading

def thread_decor(my_func):
	def wrapper(*args, **kwargs):
		my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
		my_thread.start()
	return wrapper


class Deribit:
	def __init__(self, test, only_public=False, client_ID=False, client_secret=False):
		if client_ID or client_secret: only_public = False
		if only_public:
			self.logwriter(msg='WARNING! Only public methods available!')
			return
		self.WSS_url = 'wss://www.test.deribit.com/ws/api/v2' if test else 'wss://www.deribit.com/ws/api/v2'
		self._auth(client_ID, client_secret, self.WSS_url)



	def logwriter(self, msg, filename='log.log'):
		out = datetime.now().strftime("\n[%Y%m%d,%H:%M:%S] ")+str(msg)
		print(out)
		open(filename, 'a').write(out)



	def _auth(self, client_ID, client_secret, WSS_url):
		try:
			self._WSS = create_connection(WSS_url)
			msg = {"jsonrpc" : "2.0",
				  "id" : 9929,
				  "method" : "public/auth",
				  "params" : {
					"grant_type" : "client_credentials",
					"client_id" : client_ID,
					"client_secret" : client_secret
				  }
				}
			self.logwriter('Auth OK\n############')
			print('identified')
			return self._sender(msg)
		except Exception as er:
			self.logwriter('auth error:'+str(er))



	def _sender(self, msg):
		try:
			self.logwriter(msg['method'])
			self._WSS.send(json.dumps(msg))
			out = json.loads(self._WSS.recv())
			return out['result']
		except Exception as er:
			self.logwriter(str(out))
			self.logwriter('_sender error: '+str(er))



	def make_order(self,
				side,
				instrument_name,
				amount,
				type_ord='limit',
				label=None,
				price=None,
				time_in_force='good_til_cancelled',
				max_show=False,
				post_only=True,
				reduce_only=False,
				trigger=None):
		if not side=='buy' and not side=='sell':
			self.logwriter('ERROR: incorect param "side" for make_order')
			return
		msg ={
			  "jsonrpc": "2.0",
			  "id" : 5275,
			  "method": "private/"+str(side),
			  "params": {
				"instrument_name" : instrument_name,
				"amount": amount,
				"type": type_ord,
				"label": label,
				"price": price,
				"time_in_force": time_in_force,
			   	"post_only": post_only,
			   	"reduce_only": reduce_only,
			   	"trigger":trigger}
			}
		if max_show: msg['params']['max_show'] = max_show
		return self._sender(msg)



	def edit_order(self,
				order_id,
				amount,
				price,
				post_only=True,
				stop_price=None):
		msg ={
			  "jsonrpc": "2.0",
			  "id" : 5275,
			  "method": "private/edit",
			  "params": {
			  "order_id": order_id,
				"amount": amount,
				"price": price,
			   	#"post_only": post_only,
			   	#"stop_price": stop_price
			   	}
			}
		return self._sender(msg)



	def cancel_order(self, order_id):
		msg ={
			  "jsonrpc": "2.0",
			  "id" : 5275,
			  "method": "private/cancel",
			  "params": {
				"order_id": order_id}
			}
		return self._sender(msg)



	def get_order_state(self, order_id):
		msg ={
			  "jsonrpc": "2.0",
			  "id" : 5275,
			  "method": "private/get_order_state",
			  "params": {
				"order_id": order_id}
			}
		return self._sender(msg)



	def get_order_book(self, instrument_name, depth=5):
		msg ={
		  "jsonrpc": "2.0",
		  "id" : None,
		  "method": "public/get_order_book",
		  "params": {
			"instrument_name": instrument_name,
			"depth": depth}
		}
		return self._sender(msg)

	
	
	def get_chart_data(self, instrument_name,
					start_timestamp, end_timestamp,
					resolution):
		msg ={
		  "jsonrpc": "2.0",
		  "id" : None,
		  "method": "public/get_tradingview_chart_data",
		  "params": {
			"instrument_name": instrument_name,
			"start_timestamp": start_timestamp,
			'end_timestamp': end_timestamp,
			'resolution': resolution}
		}
		return self._sender(msg)

	def get_last_trades_by_currency(self, _currency, _kind, _depth):
		msg = {
			"jsonrpc": "2.0",
			"id" : None,
			"method": "public/get_last_trades_by_currency",
			"params": {
				"currency": _currency,
				"kind" : _kind,
				"count" : _depth}
		}
		return self._sender(msg)

	def get_book_summary_by_currency(self, _currency, _kind):
		msg = \
			{
			"jsonrpc" : "2.0",
			"id" : 9344,
			"method" : "public/get_book_summary_by_currency",
			"params" : {
				"currency" : _currency,
				"kind" : _kind
				}
			}
		return self._sender(msg)
	
	@thread_decor
	def start_orderbook_update(self, instrument_name='BTC-PERPETUAL'): # current orderbook contain in 'Orderbook'
		self.__first = True
		msg = {"jsonrpc": "2.0",
			 "method": "public/subscribe",
			 "id": 42,
			 "params": {
				"channels": ["book."+str(instrument_name)+".none.1.100ms"]}
			}
		try:
			def on_message(ws, message):
				print(message)
				if self.__first: self.__first=False; return
				#self.logwriter('Orderbook')
				self.Orderbook = json.loads(message)['params']['data']
				#if func_for_quoting: func_for_quoting() # Запуск вспомогательной функции, если она есть.
			def on_error(ws, error):
				self.logwriter('Orderbook updater error: '+str(error))
			def on_close(ws):
				self.logwriter('Orderbook updater error:closed connect')
			def on_open(ws):
				ws.send(json.dumps(msg))
			websocket.enableTrace(True)
			ws = websocket.WebSocketApp(self.WSS_url,
									  on_message = on_message,
									  on_error = on_error,
									  on_close = on_close)
			ws.on_open = on_open
			ws.run_forever()
		except Exception as er:
			self.logwriter('Orderbook updater error: '+str(er))

	
'''
 You can add new methods. Example:

	def name_method(self, param1, param2):
		msg ={
		  "jsonrpc": "2.0",
		  "method": "public/METHOD",
		  "params": {
			"param1": param1,
			"param2": param2}
		}
		return self._sender(msg)
'''
