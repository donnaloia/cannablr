import requests


#Talks to the authserver
def cannablr_register(username, email, password):

	'''Takes an email and password as arguments, and sends them to the authserver via 
	an HTTP request.  The authserver will return a 200 code (success) upon succesful
	registration'''

	url="http://authserver:5000/account"
	params ={'username': username,'email': email, 'password': password}
	data = requests.post(url=url, params=params)
	if data.status_code == requests.codes.ok:
		output = data.json()
		string ="account registered"
		return string
	else:
		None

#Talks to the authserver
def cannablr_login(username, password):

	'''Takes an email and password as arguments, sends them to the authserver via an
	HTTP request.  The authserver will produce and return an authtoken via REST API
	upon succesful login'''

	url="http://authserver:5000/account/login"
	params ={'username':username, 'password':password}
	data = requests.post(url=url, params=params)
	print data.status_code
	if data.status_code == requests.codes.ok:
		test = data.json()
		return test['token']
	else:
		None

#Talks to the authserver
def validate_token(mytoken):

	'''Takes token as argument and sends it to authserver via HTTP request.  The
	authserver will unhash the token and return the users email if succesful'''

	url="http://authserver:5000/account/authenticate"
	params ={'token':mytoken}
	data = requests.post(url=url, params=params)
	if data.status_code == requests.codes.ok:
		output = data.json()
		# #pull users email from token
		userfromtoken = output['user']['username']
		return userfromtoken
	else:
		None

# Talks to the locationserver
def calculate_postalcodes(postalcode):

	'''Takes a single postal code, sends the value via HTTP request to the 
	locationserver which then calculates and returns list of the nearest 
	postal codes via REST API'''

	url="http://locationserver:8000/zipcode/"
	params ={'postalcode':postalcode}
	data = requests.post(url=url, data=params)
	output = data.json()
	zipcodes = output['postalcodes']
	return zipcodes
