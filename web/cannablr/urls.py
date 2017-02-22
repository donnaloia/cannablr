from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from accounts.views import home
from accounts.views import storefront
from accounts.views import get_entry
from accounts.views import show_reviews
from django.contrib import admin
from accounts.views import profile_listview
from accounts.views import EntryAPI
from accounts.views import UserAPI
# admin.autodiscover()

urlpatterns = [
	url(r"^$", home),
	url(r"^storefront/", storefront),
	url(r"^sell/", get_entry),
    url(r"^reviews/(?P<username1>\w+)/$", show_reviews),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/(?P<username>[\@\.\w-]+)/listview/$', profile_listview),
    url(r'^accounts/', include('userena.urls')),
    url(r'^messages/', include('django_messages.urls')),
    url(r'^api/storefront/$', EntryAPI),
    url(r'^api/users/$', UserAPI),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
