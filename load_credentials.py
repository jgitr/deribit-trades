import keyring

# Choose Backend
keyring.set_keyring([keyring.backend.get_all_keyring()][0][0])

try:
    CLIENT_ID = keyring.get_password('ubuntu', 'deribit-clientid')
    CLIENT_SECRET = keyring.get_password('ubuntu', 'deribit-clientpw')
except:
    CLIENT_ID = ''
    CLIENT_SECRET = ''
