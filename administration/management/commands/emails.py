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
        #Counts of objects associated with each Advisor
        meng_amount = 0
        msc_amount = 0
        msp_amount = 0
        mst_amount = 0
        phdbach_amount = 0
        phdmaster_amount = 0
        #Get all Advisors
        advisors = CustomUser.objects.filter(user_type__icontains="Advisor")
        #Get all sets of forms awaiting Advisor Approval
        meng_pending = MEngPOS.objects.filter(state="AdvisorPending")
        msc_pending = MSCoursePOS.objects.filter(state="AdvisorPending")
        msp_pending = MSProjectPOS.objects.filter(state="AdvisorPending")
        mst_pending = MSThesisPOS.objects.filter(state="AdvisorPending")
        phdb_pending = PHDBachelorPOS.objects.filter(state="AdvisorPending")
        phdm_pending = PHDMasterPOS.objects.filter(state="AdvisorPending")
        #Loop through advisors
        for advisor in advisors:
            logger.error("My advisor is:"+str(advisor))
            for meng in meng_pending:
                if meng.owner.advisor == advisor:
                    logger.error("MENG MATCH!")
                    meng_amount+=1
            for msc in msc_pending:
                if msc.owner.advisor == advisor:
                    logger.error("MSC MATCH!")
                    msc_amount+=1
            for msp in msp_pending:
                if msp.owner.advisor == advisor:
                    logger.error("MSP MATCH!")
                    msp_amount+=1
            for mst in mst_pending:
                if mst.owner.advisor == advisor:
                    logger.error("MST MATCH!")
                    mst_amount+=1
            for phdb in phdb_pending:
                if phdb.owner.advisor == advisor:
                    logger.error("PHDB MATCH!")
                    phdbach_amount+=1
            for phdm in phdm_pending:
                if phdm.owner.advisor == advisor:
                    logger.error("PHDM MATCH!")
                    phdmaster_amount+=1
            logger.error("MEng Amount is:"+str(meng_amount))
            logger.error("MSc Amount is:"+str(msc_amount))
            logger.error("MSp Amount is:"+str(msp_amount))
            logger.error("MSt Amount is:"+str(mst_amount))
            logger.error("PhDb Amount is:"+str(phdbach_amount))
            logger.error("PhDm Amount is:"+str(phdmaster_amount))

            #Used to check if there are 0 forms needing approval
            sum = meng_amount + msc_amount + msp_amount + mst_amount + phdbach_amount + phdmaster_amount
            logger.error("Sum is:"+str(sum))
            if (sum != 0):
                #Send Emails
                subject, from_email = 'POS Forms Need Approval', 'gradops@ece.duke.edu'
                plaintext = get_template('advisoremail.txt')
                htmly = get_template('advisoremail.html')

                recipient = advisor.email
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


            #Reinitialize Amounts
            meng_amount = 0
            msc_amount = 0
            msp_amount = 0
            mst_amount = 0
            phdbach_amount = 0
            phdmaster_amount = 0

        self.stdout.write(self.style.SUCCESS('ALL ADVISORS EMAILED'))
