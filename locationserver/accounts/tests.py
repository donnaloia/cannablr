from django.test import TestCase
from django.test import Client
from accounts.models import Entry
from accounts.forms import SellForm

class TestUser(TestCase):
    def createUser(self):
        user = User.objects.create_user('testuser', 'temporary@gmail.com', 'temporary')

    def validateLogin(self):
    	c = Client()
    	response = c.post('/accounts/signin/', {'testuser': 'john', 'password': 'temporary'})
    	response.status_code
    	self.assertEqual(response.status_code, 200)


class TestEntry(TestCase):
    def createEntry(self):
        Entry.objects.create(headline="name of some strain", body_text="bla bla bla", author="ben")
        Entry.objects.create(headline="something", body_text="bla bla bla", author="chair")

    def validateEntry(self):
        """Animals that can speak are correctly identified"""
        entry1 = Entry.objects.get(headline="name of some strain")
        entry2 = Entry.objects.get(headline="something")
        self.assertEqual(entry1.headline, 'name of some strain')
        self.assertEqual(entry2.headline, 'something')

    # def testForm(self):
    #     form_data = {'headline': 'test', 'body_text': 'description of item Im selling', 'author': 'ben'}
    #     form = SellForm(data=form_data)
    #     self.assertEqual(form.is_valid(), True)