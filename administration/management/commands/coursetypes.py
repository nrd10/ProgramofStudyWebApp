import requests
import tablib
import logging
import time
from import_export import resources
from django.core.management.base import BaseCommand, CommandError
from shared.models import CourseType
logger = logging.getLogger('administration/management/coursetypes.py')

class Command(BaseCommand):

    def handle(self, *args, **options):
        Tech, Techbool = CourseType.objects.get_or_create(title = "Approved Technical Elective")
        Elective, Electivebool = CourseType.objects.get_or_create(title = "Elective")
        self.stdout.write(self.style.SUCCESS('COURSE TYPES ADDED'))
