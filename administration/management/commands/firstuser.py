from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from shared.models import User as CustomUser
from meng.models import *
from ms.models import *
from phd.models import *
from decouple import config
import logging

logger = logging.getLogger('administration/management/firstuser.py')

#This command will email all Advisors how many forms they need to edit
class Command(BaseCommand):

    def handle(self, *args, **options):
        if CustomUser.objects.count() == 0:
            netid = 'superuser'
            password = config('password')
            superuser = CustomUser.objects.create_superuser(netid=netid, password=password)
            superuser.save()
            self.stdout.write(self.style.SUCCESS('SUPERUSER CREATED'))

        else:
            self.stdout.write(self.style.SUCCESS('SUPERUSER ALREADY EXISTS'))
