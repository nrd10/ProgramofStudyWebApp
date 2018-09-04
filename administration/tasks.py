from __future__ import absolute_import, unicode_literals
from celery import task
from celery.utils.log import get_task_logger
from shared.models import User as CustomUser
from shared.models import Course
from meng.models import *
from ms.models import *
from phd.models import *
from django.core.mail import EmailMultiAlternatives, send_mail
from django.utils.html import strip_tags
from django.template.loader import get_template, render_to_string
from django.template import Context
from django.core.management import call_command
from django.contrib import messages
from celery_progress.backend import ProgressRecorder
from async_messages import message_user, messages
from shared.models import User
from django.shortcuts import redirect

logger = get_task_logger(__name__)


@task()
def update_database(netid):
    person = User.objects.get(netid=netid)
    logger.error("My person is:"+str(person))
    call_command('updatetechnical')
    #Update Electives
    call_command('updatelective')
    # messages.success(person, "Course Update Success!")
    # messages.add_message(request, messages.INFO, "Course Update Success!")

@task()
def delete_all_courses():
    all = Course.objects.all()
    all.delete()


@task()
def populate_database(netid):
    person = User.objects.get(netid=netid)
    logger.error("My person is:"+str(person))
    # message_user(person, "Course Import START", constants.SUCCESS)
    call_command('importechnical')
    # Add Concentrations
    call_command('addconcentration')

    # Import Electives
    call_command('importelective')

    # messages.success(person, "Course Import Success!")


@task()
def email_DGS():
    #Get all DGS accounts
    DGS_accounts = CustomUser.objects.filter(user_type__icontains="DGS")

    #Get count of objects in each table awaiting DGS approval
    meng_amount = MEngPOS.objects.filter(state="DGSPending").count()
    msc_amount = MSCoursePOS.objects.filter(state="DGSPending").count()
    msp_amount = MSProjectPOS.objects.filter(state="DGSPending").count()
    mst_amount = MSThesisPOS.objects.filter(state="DGSPending").count()
    phdbach_amount = PHDBachelorPOS.objects.filter(state="DGSPending").count()
    phdmaster_amount = PHDMasterPOS.objects.filter(state="DGSPending").count()

    # logger.info("MEng Amount is:"+str(meng_amount))
    # logger.info("MSc Amount is:"+str(msc_amount))
    # logger.info("MSp Amount is:"+str(msp_amount))
    # logger.info("MSt Amount is:"+str(mst_amount))
    # logger.info("PhDb Amount is:"+str(phdbach_amount))
    # logger.info("PhDm Amount is:"+str(phdmaster_amount))

        #Loop through DGS
    for DGS in DGS_accounts:
        logger.info("My DGS is:"+str(DGS))

        #Used to check if there are 0 forms needing approval
        sum = meng_amount + msc_amount + msp_amount + mst_amount + phdbach_amount + phdmaster_amount
        logger.info("Sum is:"+str(sum))
        if (sum != 0):
            #Send Emails
            subject, from_email = 'POS Forms Need DGS Approval', 'gradops@ece.duke.edu'
            plaintext = get_template('dgsemail.txt')
            htmly = get_template('dgsemail.html')

            recipient = DGS.email
            logger.info("Recipient is:"+recipient)
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


    logger.info('ALL DGS ACCOUNTS EMAILED')




@task()
def email_advisor():
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
        logger.info("My advisor is:"+str(advisor))
        for meng in meng_pending:
            if meng.owner.advisor == advisor:
                logger.info("MENG MATCH!")
                meng_amount+=1
        for msc in msc_pending:
            if msc.owner.advisor == advisor:
                logger.info("MSC MATCH!")
                msc_amount+=1
        for msp in msp_pending:
            if msp.owner.advisor == advisor:
                logger.info("MSP MATCH!")
                msp_amount+=1
        for mst in mst_pending:
            if mst.owner.advisor == advisor:
                logger.info("MST MATCH!")
                mst_amount+=1
        for phdb in phdb_pending:
            if phdb.owner.advisor == advisor:
                logger.info("PHDB MATCH!")
                phdbach_amount+=1
        for phdm in phdm_pending:
            if phdm.owner.advisor == advisor:
                logger.info("PHDM MATCH!")
                phdmaster_amount+=1
        # logger.info("MEng Amount is:"+str(meng_amount))
        # logger.info("MSc Amount is:"+str(msc_amount))
        # logger.info("MSp Amount is:"+str(msp_amount))
        # logger.info("MSt Amount is:"+str(mst_amount))
        # logger.info("PhDb Amount is:"+str(phdbach_amount))
        # logger.info("PhDm Amount is:"+str(phdmaster_amount))

        #Used to check if there are 0 forms needing approval
        sum = meng_amount + msc_amount + msp_amount + mst_amount + phdbach_amount + phdmaster_amount
        logger.info("Sum is:"+str(sum))
        if (sum != 0):
            #Send Emails
            subject, from_email = 'POS Forms Need Approval', 'gradops@ece.duke.edu'
            plaintext = get_template('advisoremail.txt')
            htmly = get_template('advisoremail.html')

            recipient = advisor.email
            logger.info("Recipient is:"+recipient)
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

    logger.info("ALL ADVISORS EMAILED")
