import keyring
try:
    CLIENT_ID = keyring.get_password('lax', 'deribit-trades-clientid')
    CLIENT_SECRET = keyring.get_password('lax', 'deribit-trades-pw')
except:
    CLIENT_ID = ''
    CLIENT_SECRET = ''