from django.forms import ModelForm, Textarea, TextInput, RadioSelect
from accounts.models import MyProfile
from accounts.models import UserReview
from accounts.models import Entry
from django import forms


attrs_dict = {'class': 'required'}
USERNAME_RE = r'^[\.\w]+$'


class SignupForm(forms.Form):
	''' This form is for user registration and does not have an accompanying model,
	this is because when the form is filled out, the credentials are sent to the auth
	server which handles signup/login/logout/authorization'''
	username = forms.RegexField(regex=USERNAME_RE, max_length=30, widget=forms.TextInput(attrs=attrs_dict))
	email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False))


class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False))
	password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = MyProfile
        exclude = ['user', 'privacy', 'date_created']
        widgets = {
            'deliveryoption': forms.RadioSelect(choices=[
            (True, '  Yes'),
            (False, '  No')             
        ])}


class SellForm(ModelForm):
	class Meta:
		model = Entry
		fields = ['headline', 'body_text', 'entrytype', 'price1', 'price2', 'price3', 'price4', 'price5', 'item_picture']
		widgets = {
		'headline': TextInput(attrs={'data-required': 'true', 'data-parsley-maxlength':"22", 'data-parsley-maxlength-message': "You've exceeded the recommended space", 'data-parsley-trigger':"change"}),
		'body_text': Textarea(attrs={'data-parsley-minlength':"97",'data-parsley-maxlength':"252", 'data-parsley-trigger':"keyup", 'data-parsley-maxlength-message': "You've exceeded 250 characters"}),
		'price1': TextInput(attrs={'data-required': "true", 'data-parsley-maxlength':"11", 'data-parsley-trigger':"change"}),
		'price2': TextInput(attrs={'data-required': "true", 'data-parsley-maxlength':"11", 'data-parsley-trigger':"change"}),
		'entrytype': RadioSelect(choices=[
			(1, 'Strain'),
			(2, 'Tincture/Hash'),
			(3, 'Edible')
			])
		}


class UserReviewForm(ModelForm):
     class Meta:
         model = UserReview
         fields = ['stars', 'comment']
         widgets = {
         'comment': Textarea,
         'stars': RadioSelect(choices=[
         	(1, 'Very poor'),
         	(2, 'Poor'),
         	(3, 'Satisfactory'),
         	(4, 'Great'),
         	(5, 'Excellent')
         	])
         }
