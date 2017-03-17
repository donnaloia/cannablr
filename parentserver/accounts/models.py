from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.conf import settings
from django_resized import ResizedImageField
import datetime
from django.utils import timezone


class MyProfile(models.Model):
    user = models.CharField(max_length=16, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    storename=models.CharField(null=True, blank=True, max_length=20)
    streetaddress=models.CharField(null=True, blank=True, max_length=30)
    city = models.CharField(null=True, blank=True, max_length=20)
    state = models.CharField(null=True, blank=True, max_length=20)
    zipcode = models.IntegerField(_('zipcode'),
                                       null=True, blank=True)
    nearbyzips1=models.IntegerField(null=True, blank=True)
    nearbyzips2=models.IntegerField(null=True, blank=True)
    nearbyzips3=models.IntegerField(null=True, blank=True)
    nearbyzips4=models.IntegerField(null=True, blank=True)
    nearbyzips5=models.IntegerField(null=True, blank=True)
    nearbyzips6=models.IntegerField(null=True, blank=True)
    nearbyzips7=models.IntegerField(null=True, blank=True)
    nearbyzips8=models.IntegerField(null=True, blank=True)
    nearbyzips9=models.IntegerField(null=True, blank=True)
    nearbyzips10=models.IntegerField(null=True, blank=True)
    nearbyzips11=models.IntegerField(null=True, blank=True)
    nearbyzips12=models.IntegerField(null=True, blank=True)
    nearbyzips12=models.IntegerField(null=True, blank=True)
    nearbyzips13=models.IntegerField(null=True, blank=True)
    phone=models.CharField(null=True, blank=True, max_length=16)
    websiteurl=models.CharField(null=True, blank=True, max_length=38)
    deliveryoption=models.BooleanField(default=False)
    storebio=models.CharField(null=True, blank=True, max_length=100)
    storespecials=models.CharField(null=True, blank=True, max_length=65)
    reviewavg=models.FloatField(null=True, blank=True, max_length=5)
    coverpic = ResizedImageField(upload_to="site_media/media/covers/", null=True, blank=True)
    mugshot = ResizedImageField(upload_to="mugshots/", null=True, blank=True)
    privacy = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    #datetime.date.today().strftime('%b, %d %Y')


    def __unicode__(self):
        return u'%s %s %s %s %s %s %s %s' % (self.user, self.storename, self.streetaddress, self.city, self.state, self.zipcode, self.storebio, self.reviewavg)


class Entry(models.Model):
    headline= models.CharField(max_length=200,)
    body_text = models.TextField()
    author=models.ForeignKey(MyProfile, related_name='entryauthors')
    pub_date=models.DateTimeField(auto_now_add=True)
    zipcode =models.IntegerField(null=True)
    entrytype = models.IntegerField(null=True)
    price1 = models.CharField(max_length=20)
    price2 = models.CharField(max_length=20)
    price3 = models.CharField(null=True, blank=True, max_length=20)
    price4 = models.CharField(null=True, blank=True, max_length=20)
    price5 = models.CharField(null=True, blank=True, max_length=20)
    item_picture = ResizedImageField(upload_to="site_media/media/items/")

    def __str__(self):
        return u'%s %s %s %s %s %s %s' % (self.headline, self.body_text, self.pub_date, self.zipcode, self.price1, self.price2)

class UserReview(models.Model):
    name= models.ForeignKey(User, related_name='usersbeingreviewed', null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewauthors')
    pub_date=models.DateTimeField(auto_now_add=True)
    stars = models.IntegerField()
    comment = models.CharField(max_length=100)

    def __str__(self):
        return u'%s %s %s %s %s' % (self.name, self.author, self.pub_date, self.stars, self.comment)

