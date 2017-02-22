from django.core.management.base import BaseCommand, CommandError
from cities.models import *

class Command(BaseCommand):
    help = 'Removes countries other than US from db'

    def handle(self, *args, **options): 
        Country.objects.all().exclude(name='United States').delete()
        self.stdout.write(self.style.SUCCESS('Removed additional countries'))