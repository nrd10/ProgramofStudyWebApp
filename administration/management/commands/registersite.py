import requests
import tablib
import logging
import time
from import_export import resources
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from decouple import config

logger = logging.getLogger('administration/management/registersite.py')

class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            s = Site.objects.all()[0]
            s.domain = config('DOMAIN')
            s.name = config('DOMAIN')
            s.save()
            self.stdout.write(self.style.SUCCESS('SITE REGISTRATION PASSED'))


        except:
            self.stdout.write(self.style.ERROR('SITE REGISTRATION FAILED'))
