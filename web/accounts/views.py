from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import models
from django.contrib.auth.models import User
from accounts.forms import UserReviewForm
from accounts.forms import SellForm
from accounts.models import Entry
from accounts.models import UserReview
from accounts.models import MyProfile
from django.conf.urls import include, url
from django.template.loader import render_to_string
import json as simplejson
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import datetime
from userena import settings as userena_settings
from django.shortcuts import redirect, get_object_or_404
from userena.utils import signin_redirect, get_profile_model, get_user_model
from userena.views import ExtraContextTemplateView
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
	# if request.GET.get('filter') == 'deliveryyes':
	# 	latest_entries = Entry.objects.filter(author__deliveryoption=True)
	# 	context = {'latest_entries': latest_entries}
	# 	return render(request, 'storefrontload.html', context)
    return render(request, 'storefront.html', context)



def show_reviews(request, username1):
	latest_reviews = UserReview.objects.filter(name__username=username1)
	context1 = {'latest_reviews': latest_reviews}
	return render(request, 'reviews.html', context1)

@login_required
def get_entry(request):
	if request.method == 'POST':
		f = SellForm(request.POST, request.FILES)
		if f.is_valid():
			form=f.save(commit=False)
			form.author = request.user
			form.zipcode = request.user.my_profile.zipcode
			form.save()
			return HttpResponseRedirect('/accounts/{}'.format(request.user))
		else:
			print f.errors
	else:
		f = SellForm()
	return render(request, 'sell.html', {'form': f})


def profile_listview(request, username,
    template_name=userena_settings.USERENA_PROFILE_DETAIL_TEMPLATE,
    extra_context=None, **kwargs):

    """
    note: 'extra_context' is a dictionary of variables which should be supplied to the template.
    """

    user = get_object_or_404(get_user_model(),
                             username__iexact=username)
    fullsalelist = Entry.objects.filter(author__username__iexact=username).order_by('-pub_date')
    userreviews = UserReview.objects.filter(name__username__iexact=username).order_by('-pub_date')

    if request.is_ajax():
      	object_name = request.POST.get('entryname')
      	targetobject = Entry.objects.get(headline=object_name)
      	if request.user.username == targetobject.author.username:
         	targetobject.delete()
      	return HttpResponseRedirect('/storefront/')
    
   

    profile_model = get_profile_model()
    try:
        profile = user.my_profile
    except profile_model.DoesNotExist:
        profile = profile_model.objects.create(user=user)

    if not profile.can_view_profile(request.user):
        raise PermissionDenied
    if not extra_context: extra_context = dict()
    
    if username == request.user.username:
        pageowner="True"
        extra_context['pageowner'] = pageowner
    extra_context['profile'] = user.my_profile
    extra_context['fullsalelist'] = fullsalelist
    extra_context['userreviews'] = userreviews
    extra_context['hide_email'] = userena_settings.USERENA_HIDE_EMAIL
    
    return ExtraContextTemplateView.as_view(template_name='profile_listview.html',
                                            extra_context=extra_context)(request)



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
