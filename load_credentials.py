import keyring

# Choose Backend
keyring.set_keyring([keyring.backend.get_all_keyring()][0][0])

try:
    CLIENT_ID = keyring.get_password('lax', 'deribit-trades-clientid')
    CLIENT_SECRET = keyring.get_password('lax', 'deribit-trades-pw')
except:
    CLIENT_ID = ''
    CLIENT_SECRET = ''
