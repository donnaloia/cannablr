from django.shortcuts import render
from django.shortcuts import redirect
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
    '''if user is logged in they will be directed to the storefront, otherwise all visitors will be directed
    to the cannablr landing page'''
    if 'username' in request.session:
        return redirect('/storefront')
    else:
        return render(request, 'homepage.html')


def storefront(request):
    '''handles the storefront which is the main page for cannablr.com, this page
    displays all items for sale based on location.'''
    if 'username' in request.session:
        if MyProfile.objects.filter(user=request.session['username']).exists():
            active_user = MyProfile.objects.get(user=request.session['username'])
            if active_user.zipcode:
                latest_entries = Entry.objects.filter(zipcode__in=[active_user.nearbyzips1,
                active_user.nearbyzips2,
                active_user.nearbyzips3,
                active_user.nearbyzips4,
                active_user.nearbyzips5,
                active_user.nearbyzips6,
                active_user.nearbyzips7,
                active_user.nearbyzips8,
                active_user.nearbyzips9,
                active_user.nearbyzips10,
                active_user.nearbyzips11,
                active_user.nearbyzips12]).order_by('-pub_date')[:16]
                context = {'latest_entries': latest_entries, 'active_user': active_user}        
            else:
                latest_entries = Entry.objects.order_by('-pub_date')[:16]
                context = {'latest_entries': latest_entries, 'active_user': active_user}
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
    '''handles user account signup'''
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            cannablr_register(username, email, password)
            active_token = cannablr_login(username, password)
            validated_user = validate_token(active_token)
            request.session['active_token'] = active_token
            request.session['username'] = validated_user
            return HttpResponseRedirect('/accounts/signup/complete')
    else:
        form = SignupForm()
        return render(request, 'signup_form.html', {'form': form})


def login(request):
    '''handles user account login'''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username, password = (form.cleaned_data['username'],
                                                     form.cleaned_data['password'])
            active_token = cannablr_login(username, password)
            validated_user = validate_token(active_token)
            request.session['active_token'] = active_token
            request.session['username'] = validated_user
            return redirect('/accounts/{}'.format(request.session['username']))
    else:
        form = LoginForm()
    return render(request, 'login_form.html', {'form': form})

def logout(request):
    '''logs user out'''
    try:
        del request.session['username']
    except:
        pass
    # add code here to expire token on authserver
    return render(request, 'signout.html')


def profile_edit(request, username):
    '''handles the profile edit form and POST request'''
    #TODO:  Add logic to check for profile, then edit existing, rather than try to create a duplicate profile
    if request.session['username'] != username:
        return redirect("/accounts/login")
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
            profile.save()
            return redirect('/accounts/{}'.format(request.session['username']))
    else:
        form = ProfileForm()
    return render(request, 'edit_profile.html', {'form': form})


def profile_detail(request, username):
    '''handles all the logic required to display a users profile page'''
    if 'username' in request.session:
        if MyProfile.objects.filter(user=request.session['username']).exists():
            active_user = MyProfile.objects.get(user=request.session['username'])
            if request.method == 'POST':
                form = UserReviewForm(request.POST)
                users_profile = MyProfile.objects.get(user=username)
                if form.is_valid():
                    reviewform=form.save(commit=False)
                    reviewform.name=users_profile.user
                    reviewform.author=active_user.user
                    reviewform.save()
                    staravg = UserReview.objects.filter(name__user=username).aggregate(Avg('stars'))
                    users_profile.reviewavg=staravg['stars__avg']
                    users_profile.save()
                    return redirect('/accounts/{}'.format(users_profile.user))

    if MyProfile.objects.filter(user=username).exists():
        form = UserReviewForm()
        #refactor this line out - replace with active_user above
        profile = MyProfile.objects.get(user=username)
        hotsellers = Entry.objects.filter(author__user=username)[:4]
        userreviews = UserReview.objects.filter(name__username=username)
        return render(request, 'profile_detail.html', {'profile': profile, 'hotsellers': hotsellers, 'userreviews': userreviews, 'form': form})
    
    else:
        return redirect('/storefront')


def profile_listview(request, username):
    '''an extended profile view where items are listed in a grid rather than visual snapshots'''
    if 'username' in request.session:
        if MyProfile.objects.filter(user=request.session['username']).exists():
            active_user = MyProfile.objects.get(user=request.session['username'])
            if request.method == 'POST':
                form = UserReviewForm(request.POST)
                users_profile = MyProfile.objects.get(user=username)
                if form.is_valid():
                    reviewform=form.save(commit=False)
                    reviewform.name=users_profile.user
                    reviewform.author=active_user.user
                    reviewform.save()
                    staravg = UserReview.objects.filter(name__user=username).aggregate(Avg('stars'))
                    users_profile.reviewavg=staravg['stars__avg']
                    users_profile.save()
                    return redirect('/accounts/{}'.format(users_profile.user))

    if MyProfile.objects.filter(user=username).exists():
        form = UserReviewForm()
        profile = MyProfile.objects.get(user=username)
        fullsalelist = Entry.objects.filter(author__user=username).order_by('-pub_date')
        userreviews = UserReview.objects.filter(name__username=username)
        return render(request, 'profile_detail.html', {'profile': profile, 'hotsellers': hotsellers, 'userreviews': userreviews, 'form': form})
    
    if request.is_ajax():
        object_name = request.POST.get('entryname')
        targetobject = Entry.objects.get(headline=object_name)
        if request.session['username'] == targetobject.author.user:
            targetobject.delete()
            return HttpResponseRedirect('/storefront/')


def show_reviews(request, username1):
    '''returns user reviews'''
    latest_reviews = UserReview.objects.filter(name__user=username1)
    context1 = {'latest_reviews': latest_reviews}
    return render(request, 'reviews.html', context1)


def get_entry(request):
    '''handles form for posting itmems for sale'''
    if MyProfile.objects.filter(user=request.session['username']).exists():
        active_user = MyProfile.objects.get(user=request.session['username'])
    else:
        return redirect("/accounts/login")
    if request.method == 'POST':
        form = SellForm(request.POST, request.FILES)
        if form.is_valid():
            form=form.save(commit=False)
            print request.session['username']
            form.author = active_user
            form.zipcode = active_user.zipcode
            form.save()
            return redirect('/accounts/{}'.format(request.session['username']))
        else:
            print form.errors
    else:
        form = SellForm()
    return render(request, 'sell.html', {'form': form, 'active_user': active_user})


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