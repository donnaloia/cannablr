from django.forms import ModelForm, Textarea, TextInput, RadioSelect
from accounts.models import UserReview
from accounts.models import Entry
from django import forms

# Create the form class.
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
