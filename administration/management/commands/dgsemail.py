import requests
import tablib
import logging
import time
from import_export import resources
from django.core.management.base import BaseCommand, CommandError
from shared.models import User as CustomUser
from meng.models import *
from ms.models import *
from phd.models import *
from collections import OrderedDict
from django.db.models import Q #allows for complex queries
from django.core.mail import EmailMultiAlternatives, send_mail
from django.utils.html import strip_tags
from django.template.loader import get_template, render_to_string
from django.template import Context

logger = logging.getLogger('administration/management/emails.py')


#This command will email all Advisors how many forms they need to edit
class Command(BaseCommand):

    def handle(self, *args, **options):
        #Get all DGS accounts
        DGS_accounts = CustomUser.objects.filter(user_type__icontains="DGS")

        #Get count of objects in each table awaiting DGS approval
        meng_amount = MEngPOS.objects.filter(state="DGSPending").count()
        msc_amount = MSCoursePOS.objects.filter(state="DGSPending").count()
        msp_amount = MSProjectPOS.objects.filter(state="DGSPending").count()
        mst_amount = MSThesisPOS.objects.filter(state="DGSPending").count()
        phdbach_amount = PHDBachelorPOS.objects.filter(state="DGSPending").count()
        phdmaster_amount = PHDMasterPOS.objects.filter(state="DGSPending").count()

        logger.error("MEng Amount is:"+str(meng_amount))
        logger.error("MSc Amount is:"+str(msc_amount))
        logger.error("MSp Amount is:"+str(msp_amount))
        logger.error("MSt Amount is:"+str(mst_amount))
        logger.error("PhDb Amount is:"+str(phdbach_amount))
        logger.error("PhDm Amount is:"+str(phdmaster_amount))

        #Loop through DGS
        for DGS in DGS_accounts:
            logger.error("My DGS is:"+str(DGS))

            #Used to check if there are 0 forms needing approval
            sum = meng_amount + msc_amount + msp_amount + mst_amount + phdbach_amount + phdmaster_amount
            logger.error("Sum is:"+str(sum))
            if (sum != 0):
                #Send Emails
                subject, from_email = 'POS Forms Need DGS Approval', 'gradops@ece.duke.edu'
                plaintext = get_template('dgsemail.txt')
                htmly = get_template('dgsemail.html')

                recipient = DGS.email
                logger.error("Recipient is:"+recipient)
                d = { 'meng': meng_amount,
                'msc': msc_amount,
                'msp': msp_amount,
                'mst': mst_amount,
                'phdb': phdbach_amount,
                'phdm': phdmaster_amount }

                text_content = plaintext.render(d)
                html_content = htmly.render(d)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
                msg.attach_alternative(html_content, "text/html")
                msg.send()


        self.stdout.write(self.style.SUCCESS('ALL DGS ACCOUNTS EMAILED'))
