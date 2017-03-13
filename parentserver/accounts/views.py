from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import models
from django.contrib.auth.models import User
from accounts.forms import UserReviewForm
from accounts.forms import SellForm
from accounts.forms import SignupForm
from accounts.forms import LoginForm
from accounts.forms import ProfileForm
from accounts.models import Entry
from accounts.models import UserReview
from accounts.models import MyProfile
from django.conf.urls import include, url
from django.template.loader import render_to_string
import json as simplejson
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import datetime
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django_messages.models import inbox_count_for
from django.contrib.auth.views import login
from accounts.serializers import EntrySerializer
from accounts.serializers import UserSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from accounts.api_consumer import cannablr_register, cannablr_login, validate_token, calculate_postalcodes




def home(request):
    if request.user.is_authenticated():
        return redirect('/storefront')
    else:
        return render(request, 'homepage.html')


def storefront(request):
    if request.user.is_authenticated():
        if request.user.my_profile.zipcode:
            latest_entries = Entry.objects.filter(zipcode__in=[request.user.my_profile.nearbyzips1,
            request.user.my_profile.nearbyzips2,
            request.user.my_profile.nearbyzips3,
            request.user.my_profile.nearbyzips4,
            request.user.my_profile.nearbyzips5,
            request.user.my_profile.nearbyzips6,
            request.user.my_profile.nearbyzips7,
            request.user.my_profile.nearbyzips8,
            request.user.my_profile.nearbyzips9,
            request.user.my_profile.nearbyzips10,
            request.user.my_profile.nearbyzips11,
            request.user.my_profile.nearbyzips12]).order_by('-pub_date')[:16]
            unread_list = inbox_count_for(request.user)
            context = {'latest_entries': latest_entries, 'unread_list': unread_list}        
        else:
            latest_entries = Entry.objects.order_by('-pub_date')[:16]
            context = {'latest_entries': latest_entries}
    else:
        latest_entries = Entry.objects.order_by('-pub_date')[:16]
        context = {'latest_entries': latest_entries} 
    if request.is_ajax():
	    if request.GET.get('filter') == 'strains':
		    latest_entries = latest_entries.filter(entrytype=1)
		    context = {'latest_entries': latest_entries}
		    return render(request, 'storefrontload.html', context)
	    if request.GET.get('filter') == 'concentrates':
		    latest_entries = Entry.objects.filter(entrytype=2)
		    context = {'latest_entries': latest_entries}
		    return render(request, 'storefrontload.html', context)
	    if request.GET.get('filter') == 'edibles':
		    latest_entries = Entry.objects.filter(entrytype=3)
		    context = {'latest_entries': latest_entries}
		    return render(request, 'storefrontload.html', context)
    return render(request, 'storefront.html', context)


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            cannablr_register(username, email, password)
            active_token = cannablr_login(username, password)
            request.session['active_token'] = active_token
            request.session['username'] = username
            return HttpResponseRedirect('/accounts/signup/complete')
    else:
        form = SignupForm()
    return render(request, 'signup_form.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username, password = (form.cleaned_data['username'],
                                                     form.cleaned_data['password'])
            active_token = cannablr_login(username, password)
            request.session['active_token'] = active_token
            request.sesion['username'] = username
            return HttpResponseRedirect('/accounts/{}'.format(request.username))
    else:
        form = LoginForm()
    return render(request, 'login_form.html', {'form': form})


def profile_edit(request, username):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            cleanzipcode= form.cleaned_data['zipcode']
            zip_codes=calculate_postalcodes(cleanzipcode)
            profile=form.save(commit=False)
            profile.user = request.session['username']
            profile.nearbyzips1 = zip_codes[0]
            profile.nearbyzips2 = zip_codes[1]
            profile.nearbyzips3 = zip_codes[2]
            profile.nearbyzips4 = zip_codes[3]
            profile.nearbyzips5 = zip_codes[4]
            profile.nearbyzips6 = zip_codes[5]
            profile.nearbyzips7 = zip_codes[6]
            profile.nearbyzips8 = zip_codes[7]
            profile.nearbyzips9 = zip_codes[8]
            profile.nearbyzips10 = zip_codes[9]
            profile.nearbyzips11 = zip_codes[10]
            profile.nearbyzips12 = zip_codes[11]
            profile = form.save()
            return HttpResponseRedirect('/accounts/{}'.format(request.session['username']))
    else:
        form = ProfileForm()
    return render(request, 'edit_profile.html', {'form': form})


def profile_detail(request, username):
    # if request.method == 'POST':
    #     form = UserReviewForm(request.POST)
    #     tester1 = User.objects.get(username=username)
    #     if form.is_valid():
    #         reviewform=form.save(commit=False)
    #         reviewform.name=tester1
    #         reviewform.author=request.user
    #         reviewform.save()
    #         staravg = UserReview.objects.filter(name__username__iexact=username).aggregate(Avg('stars'))
    #         h = MyProfile.objects.get(user__username__iexact=username)
    #         h.reviewavg=staravg['stars__avg']
    #         h.save()
    #         return redirect('/accounts/{}'.format(tester1))
    # else:
    form = UserReviewForm()
    profile_info = MyProfile.objects.filter(user=username)
    hotsellers = Entry.objects.filter(author__user=username)[:4]
    userreviews = UserReview.objects.filter(name__username=username)
    return render(request, 'profile_detail.html', {'profile': profile_info, 'hotsellers': hotsellers, 'userreviews': userreviews, 'form': form})


def show_reviews(request, username1):
	latest_reviews = UserReview.objects.filter(name__username=username1)
	context1 = {'latest_reviews': latest_reviews}
	return render(request, 'reviews.html', context1)


def get_entry(request):
	if request.method == 'POST':
		f = SellForm(request.POST, request.FILES)
		if f.is_valid():
			form=f.save(commit=False)
			form.author = request.session['username']
			active_user = MyProfile.objects.filter(user=request.session['username'])
			form.zipcode = active_user['zipcode']
			form.save()
			return HttpResponseRedirect('/accounts/{}'.format(request.session['username']))
		else:
			print f.errors
	else:
		f = SellForm()
	return render(request, 'sell.html', {'form': f})


# def profile_listview(request, username,
#     template_name=userena_settings.USERENA_PROFILE_DETAIL_TEMPLATE,
#     extra_context=None, **kwargs):

#     """
#     note: 'extra_context' is a dictionary of variables which should be supplied to the template.
#     """

#     user = get_object_or_404(get_user_model(),
#                              username__iexact=username)
#     fullsalelist = Entry.objects.filter(author__username__iexact=username).order_by('-pub_date')
#     userreviews = UserReview.objects.filter(name__username__iexact=username).order_by('-pub_date')

#     if request.is_ajax():
#       	object_name = request.POST.get('entryname')
#       	targetobject = Entry.objects.get(headline=object_name)
#       	if request.user.username == targetobject.author.username:
#          	targetobject.delete()
#       	return HttpResponseRedirect('/storefront/')
    
   

#     profile_model = get_profile_model()
#     try:
#         profile = user.my_profile
#     except profile_model.DoesNotExist:
#         profile = profile_model.objects.create(user=user)

#     if not profile.can_view_profile(request.user):
#         raise PermissionDenied
#     if not extra_context: extra_context = dict()
    
#     if username == request.user.username:
#         pageowner="True"
#         extra_context['pageowner'] = pageowner
#     extra_context['profile'] = user.my_profile
#     extra_context['fullsalelist'] = fullsalelist
#     extra_context['userreviews'] = userreviews
#     extra_context['hide_email'] = userena_settings.USERENA_HIDE_EMAIL
    
#     return ExtraContextTemplateView.as_view(template_name='profile_listview.html',
#                                             extra_context=extra_context)(request)



#Public REST API (Not yet completed)

@api_view(['GET'])
@csrf_exempt
def EntryAPI(request):
    listofitemsforsale = Entry.objects.all()
    serializer = EntrySerializer(listofitemsforsale, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes((BasicAuthentication,))
@permission_classes((IsAuthenticated,))
def UserAPI(request):
    userlist = MyProfile.objects.all()
    serializer = UserSerializer(userlist, many=True)
    return Response(serializer.data)