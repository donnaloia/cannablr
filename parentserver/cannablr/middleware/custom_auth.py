from accounts.api_consumer import cannablr_register, cannablr_login, validate_token

def process_request(self, request):
	if request.token = None:
		pass:
	else:
		username = validate_token(request.token)
    	request.username = username