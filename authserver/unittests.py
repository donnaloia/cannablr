# run with:
# python -m unittest discover -p "*unittests.py"
from app import app
import logging
import unittest
import json


# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

######################################################################
#  T E S T   C A S E S
######################################################################
class TestAuthServer(unittest.TestCase):

    def setUp(self):
        app.debug = True
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.CRITICAL)
        self.app = app.test_client()

    def test_index(self):
        resp = self.app.get('/', data=data)
        self.assertTrue( resp.status_code != HTTP_200_OK )

    def test_create_user(self):
        # save the current number of pets for later comparrison
        new_account = {'email': 'benjini', 'password': 'baggio'}
        data = json.dumps(new_account)
        resp = self.app.post('/account', data=data)
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        # Check the data is correct
        new_json = json.loads(resp.data)
        self.assertEqual (new_json['email'], 'benjo')
######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
