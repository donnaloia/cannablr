from django.test import TestCase
from accounts.models import MyProfile
from django.contrib.auth.models import User

class AccountTestCase(TestCase):
    def setUp(self):
    	johnlennon = User.objects.create_user(username='john',
                                 email='jlennon@beatles.com',
                                 password='glassonion')
        MyProfile.objects.create(user=johnlennon, storename="John Lennon rules", zipcode=97202, phone="503-407-4552", websiteurl="www.benisdabomb.com")
        

    def test_create_user(self):
        """Create User record and retrieve said record"""
        jlennonprofile = MyProfile.objects.get(user__username="john")
        self.assertEqual(jlennonprofile.storename, "John Lennon rules")