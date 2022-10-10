import keyring

    
# Choose Backend
keyring.set_keyring([keyring.backend.get_all_keyring()][0][0])

print('Enter a filename to store your CLIENTID')
clientid_name = input()

print('Enter a filename to store your Password')
password_name = input()

print('Enter your system username (e.g. root)')
username = input()

print('Enter your Deribit CLIENTID')
clientid = input()

print('Enter your Deribit Password')
password = input()

print('Saving credentials...')
keyring.set_password(username, clientid_name, clientid)
keyring.set_password(username, password_name, password)

retrieve_clientid = 'keyring.get_password({}, {})'.format(str(username), str(clientid_name))
retrieve_password = 'keyring.get_password({}, {})'.format(str(username), str(password_name))

print('Paste the following commands in the given order in load_credentials.py under CLIENT_ID and CLIENT_SECRET')
print(retrieve_clientid)
print(retrieve_password)

