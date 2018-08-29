import requests
import tablib
import logging
import time
from import_export import resources
from decouple import config
from django.core.management.base import BaseCommand, CommandError
from shared.models import Course
from administration.resources import CourseResource, CourseUpdate
from collections import OrderedDict
logger = logging.getLogger('administration/management/importelective.py')
#Global Variables: ACCESS TOKEN --> THIS CAN CHANGE
TOKEN = config('TOKEN')

#RUN TIME:

#Function to Replaces Spaces With Token usable for Requests to Each Constructed URL
def replace_token_inplace(s, token=" "):
    for index, char in enumerate(s):
        if ord(char) == ord(token):
            s[index] = '%20'
    return s

#Below function gets all ELECTIVE URLS
def get_urls():
    subject_url ="https://streamer.oit.duke.edu/curriculum/list_of_values/fieldname/SUBJECT?access_token="
    called_url = subject_url+TOKEN
    r = requests.get(called_url)
    x = r.json()
    #Get the list inside of series of dictionaries received from request
    first_key = x['scc_lov_resp']
    second_key = first_key['lovs']
    third_key = second_key['lov']
    fourth_key = third_key['values']
    mylist = fourth_key['value']
    counter = 0
    classes = []
    x = ''

    #Append classes
    finalcount = 0
    for dict in mylist:
         for item in dict.items():
             if (counter == 0):
                 x += str(dict['code'])
                 counter = counter + 1
             if (counter == 1):
                 x += ' - '
                 counter = counter + 1
                 x += str(dict['desc'])
             if (counter == 2):
                 classes.append(x)
                 x = ''
                 counter = 0
             finalcount = finalcount + 1

    #Replaces spaces in each listing and deletes subjects that return no classes in API
    edits = []
    for item in classes:
        if (('@' in item) or ('(' in item) or ("INCU" in item) or ("INCS" in item)
        or ("INCH" in item) or ("INCG" in item) or ("INCC" in item) or ("JGER" in item)
        or ("KICHE" in item) or ("PATHASST" in item) or ("PTA" in item)
        or ("ROBT" in item) or ("ZZZ" in item) or ("ZOO" in item)
        or ("ECE" in item) or ("MATH" in item) or ("PHYSICS" in item)
        or ("STA" in item) or ("COMPSCI" in item) or ("CHEM" in item)
        or ("ECE" in item) or ("ENERGYEGR" in item)
        or ("CEE" in item) or ("ADF" in item)):
            del(item)
            continue
        s = list(item)
        replace_token_inplace(s)
        z = ''.join(s)
        edits.append(z)

    # strings to build URL to make request from for classes
    begin = "https://streamer.oit.duke.edu/curriculum/courses/subject/"
    ending = "?access_token=94fbc0640ed3e6e2e70f942dd4867a33"
    #Get only unique URLS
    finaledits = list(OrderedDict.fromkeys(edits))
    #list holding final URLS
    mylist = []
    f = open("subjecturls.txt", "w")
    for index in finaledits:
        x = begin+index+ending
        mylist.append(x)

    return mylist



class Command(BaseCommand):

    def handle(self, *args, **options):
        #TECHNICAL ELECTIVE SUBJECTS: MATH, STA, COMPSCI, PHYSICS, CHEM, ECE, ME, ENERGYEGR, CEE
        #Hardcoded Technical URLS

        electives = get_urls()
        for url in electives:
            r = requests.get(url)
            #Check for 404 response --> skip if 404
            if r.status_code == 404:
                logger.error("GOT 404 STATUS CODE --> SKIP")
                continue

            if r.status_code == 500:
                logger.error("GOT 500 STATUS CODE --> SKIP SERVER ERROR")
                continue

            x = r.json()
            first_key = x['ssr_get_courses_resp']
            second_key = first_key['course_search_result']
            message = second_key['ssr_crs_gen_msg']

            #Key to check to determine if this entry should be skipped or not
            if message is not None:
                print("REQUEST RETURNED NULL --> SKIP")
                continue

            #Issues With Dictionary for Subjects with One Class --> skip
            if second_key['ssr_crs_srch_count'] == "1":
                print("ONLY ONE CLASS --> SKIP")
                continue

            third_key = second_key['subjects']
            fourth_key = third_key['subject']
            fifth_key = fourth_key['course_summaries']
            SUBJECT = fourth_key['subject']
            logger.error("SUBJECT IS: "+SUBJECT)
            mylist = fifth_key['course_summary']

            elective = "Elective"

            #Create TABLIB Dataset
            headers = ('id', 'listing', 'title', 'category', 'concentration', 'term')
            dataset = tablib.Dataset([], headers=headers)
            for dict in mylist:
                if "L9" in dict['catalog_nbr']:
                    continue
                else:
                    listing = dict['subject']+" "+dict['catalog_nbr']
                    title = dict['course_title_long']
                    term = dict['ssr_crse_typoff_cd']
                    if term is  None:
                        term = "UNKNOWN"
                        # print("Listing: "+listing+" Title: "+title+" Term: "+term)
                        dataset.append(('', listing, title, elective, '', term))

            #Delete 1st row as it is empty
            del dataset[0]

            #Print Dataset
            # print("My dataset is:")
            # print(dataset.export('csv'))
            self.stdout.write(self.style.SUCCESS('DATA WRANGLING SUCCESS'))

        # Import dataset into database
            course_resource = CourseUpdate()

        #DRY RUN of import
            result = course_resource.import_data(dataset, dry_run=True)
            if result.has_errors():
                self.stdout.write(self.style.ERROR('DRY RUN FAILED'))
                exit()
            else:
                self.stdout.write(self.style.SUCCESS('DRY RUN PASSED'))

        # Actual import
            true_import = course_resource.import_data(dataset, dry_run=False)
            if true_import.has_errors():
                self.stdout.write(self.style.ERROR('IMPORT FAILURE'))
                exit()
            else:
                self.stdout.write(self.style.SUCCESS('IMPORT SUCCESS'))

        self.stdout.write(self.style.SUCCESS('ALL API IMPORT UPDATES PASSED'))
