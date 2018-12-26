import requests
import tablib
import logging
import time
from import_export import resources
from django.core.management.base import BaseCommand, CommandError
from shared.models import Course, CourseType
logger = logging.getLogger('administration/management/590courses.py')

class Command(BaseCommand):

    def handle(self, *args, **options):
        # Course Types to Add
        Elective, Electivebool = CourseType.objects.get_or_create(title = "Elective")
        Tech, Techbool = CourseType.objects.get_or_create(title = "Approved Technical Elective")


        first, firstbool = Course.objects.get_or_create(listing = "ECE 590-01",
        title="Special Topics", term="UNKOWN")
        first.category.add(Elective)
        first.category.add(Tech)

        second, secondbool = Course.objects.get_or_create(listing = "ECE 590-02",
        title="Special Topics", term="UNKOWN")
        second.category.add(Elective)
        second.category.add(Tech)

        third, thirdbool = Course.objects.get_or_create(listing = "ECE 590-03",
        title="Special Topics", term="UNKOWN")
        third.category.add(Elective)
        third.category.add(Tech)

        fourth, fourthbool = Course.objects.get_or_create(listing = "ECE 590-04",
        title="Special Topics", term="UNKOWN")
        fourth.category.add(Elective)
        fourth.category.add(Tech)

        fifth, fifthbool = Course.objects.get_or_create(listing = "ECE 590-05",
        title="Special Topics", term="UNKOWN")
        fifth.category.add(Elective)
        fifth.category.add(Tech)

        sixth, sixthbool = Course.objects.get_or_create(listing = "ECE 590-06",
        title="Special Topics", term="UNKOWN")
        sixth.category.add(Elective)
        sixth.category.add(Tech)

        seventh, seventhbool = Course.objects.get_or_create(listing = "ECE 590-07",
        title="Special Topics", term="UNKOWN")
        seventh.category.add(Elective)
        seventh.category.add(Tech)

        eighth, eighthbool = Course.objects.get_or_create(listing = "ECE 590-08",
        title="Special Topics", term="UNKOWN")
        eighth.category.add(Elective)
        eighth.category.add(Tech)

        ninth, ninthbool = Course.objects.get_or_create(listing = "ECE 590-09",
        title="Special Topics", term="UNKOWN")
        ninth.category.add(Elective)
        ninth.category.add(Tech)

        tenth, tenthbool = Course.objects.get_or_create(listing = "ECE 590-10",
        title="Special Topics", term="UNKOWN")
        tenth.category.add(Elective)
        tenth.category.add(Tech)

        eleventh, eleventhbool = Course.objects.get_or_create(listing = "ECE 590-11",
        title="Special Topics", term="UNKOWN")
        eleventh.category.add(Elective)
        eleventh.category.add(Tech)


        self.stdout.write(self.style.SUCCESS('590 COURSES ADDED'))
