import requests
def calculate_postalcodes(postalcode):
	url="http://locationserver:8000/zipcode/"
	params ={'postalcode':postalcode}
	data = requests.post(url=url, data=params)
	output = data.json()
	zipcodes = output['postalcodes']
	return zipcodes


def validate_token(mytoken):
	url="http://172.17.0.3:5000/account/authenticate"
	params ={'token':mytoken}
	data = requests.post(url=url, params=params)
	if data.status_code == requests.codes.ok:
		output = data.json()
		# #pull users email from token
		userfromtoken = output['user']['email']
		return userfromtoken
	else:
		None

