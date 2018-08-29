import requests
import tablib
import logging
import time
from import_export import resources
from django.core.management.base import BaseCommand, CommandError
from shared.models import Course, Concentration
from phd.models import CurricularArea
from collections import OrderedDict
from django.db.models import Q #allows for complex queries
logger = logging.getLogger('administration/management/addconcentration.py')


#This command will add concentration each course
class Command(BaseCommand):

    def handle(self, *args, **options):

        #Concentration Course Lists --> hardcoded because it is unavailable through the API
        CE = ["ECE  538", "ECE  539", "ECE  552", "ECE  553", "ECE  554", "ECE  555",
        "ECE  556", "ECE  557", "ECE  558", "ECE  559", "ECE  561", "ECE  562", "ECE  611",
        "ECE  650", "ECE  651", "ECE  652"]
        MNS = ["ECE  511", "ECE  521", "ECE  526", "ECE  528", "ECE  529", "ECE  531",
        "ECE  532", "ECE  537", "ECE  539", "ECE  631"]
        PH = ["ECE  521", "ECE  523", "ECE  541", "ECE  545", "ECE  546", "ECE  722"]
        SW = ["ECE  571", "ECE  572", "ECE  573", "ECE  574", "ECE  575", "ECE  577",
        "ECE  578", "ECE  675", "ECE  676"]
        SPC = ["ECE  581", "ECE  582", "ECE  584", "ECE  585", "ECE  587", "ECE  681",
        "ECE  683", "ECE  686", "ECE  688"]
        #Concentration Objects
        Comp, Compbool = Concentration.objects.get_or_create(title = "Computer Engineering")
        Micro, Microbool = Concentration.objects.get_or_create(title = "Micro-Nano Systems")
        Photo, Photobool = Concentration.objects.get_or_create(title = "Photonics")
        Sense, Sensebool = Concentration.objects.get_or_create(title = "Sensing & Waves")
        Signal, Signalbool = Concentration.objects.get_or_create(title = "Signal Processing & Communications")


        MN, MNbool = CurricularArea.objects.get_or_create(title = "Microelectronics, Photonics, and Nanotechnology")
        PHY, PHYbool = CurricularArea.objects.get_or_create(title = "Engineering Physics")
        CENG, CENGbool = CurricularArea.objects.get_or_create(title = "Computer Engineering")
        SGN, SGNbool = CurricularArea.objects.get_or_create(title = "Signal & Information Processing")
        self.stdout.write(self.style.SUCCESS('CURRICULAR AREAS ADDED'))


        i = 0
        while i < len(CE):
            obj = Course.objects.get(Q(listing__iexact=CE[i]))
            obj.concentration.add(Comp)
            obj.save()
            i+=1

        self.stdout.write(self.style.SUCCESS('COMP ARCH CONCENTRATIONS ADDED'))

        i = 0
        while i < len(MNS):
            obj = Course.objects.get(Q(listing__iexact=MNS[i]))
            obj.concentration.add(Micro)
            obj.save()
            i+=1

        self.stdout.write(self.style.SUCCESS('MICRO NANO SYSTEMS CONCENTRATIONS ADDED'))

        i = 0
        while i < len(PH):
            obj = Course.objects.get(Q(listing__iexact=PH[i]))
            obj.concentration.add(Photo)
            obj.save()
            i+=1

        self.stdout.write(self.style.SUCCESS('PHOTONICS CONCENTRATIONS ADDED'))

        i = 0
        while i < len(SW):
            obj = Course.objects.get(Q(listing__iexact=SW[i]))
            obj.concentration.add(Sense)
            obj.save()
            i+=1

        self.stdout.write(self.style.SUCCESS('SENSING & WAVES CONCENTRATIONS ADDED'))

        i = 0
        while i < len(SPC):
            obj = Course.objects.get(Q(listing__iexact=SPC[i]))
            obj.concentration.add(Signal)
            obj.save()
            i+=1

        self.stdout.write(self.style.SUCCESS('SIGNAL PROCESSING CONCENTRATIONS ADDED'))

        self.stdout.write(self.style.SUCCESS('ALL CONCENTRATIONS ADDED'))
