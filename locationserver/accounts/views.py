import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import models
from django.contrib.auth.models import User
from django.conf.urls import include, url
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from cities.models import PostalCode
from django.http import JsonResponse


###  Helper Functions ###
def location_query(postalcode):
	nearestzips = PostalCode.objects.distance(PostalCode.objects.get(code=postalcode).location).order_by('distance')[:12]
	zip_codes = list(nearestzips.values_list('code', flat=True))
	return zip_codes

###  View Functions  ###
@csrf_exempt
def showzippy(request):
	if request.method == 'POST':
		mypostalcode = request.POST['postalcode']
		postalcodez = location_query(mypostalcode)

		context = {'zipcodes': postalcodez}
		return JsonResponse({'postalcodes':postalcodez})
	else:
		context = {'zipcodes': 'we dont have any'}
		return render(request, 'test.html', context)