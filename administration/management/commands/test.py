import requests
import tablib
from import_export import resources
from django.core.management.base import BaseCommand, CommandError
from shared.models import Course, CourseType
from administration.resources import CourseResource
from django.db.models import Q #allows for complex queries
import logging
logger = logging.getLogger('administration/management/updatetechnical.py')
#Global Variables: ACCESS TOKEN --> THIS CAN CHANGE
TOKEN = "94fbc0640ed3e6e2e70f942dd4867a33"
# Courses: ID, Listing, Title, Category (Elective vs Approved Technical Elective), Concentration

class Command(BaseCommand):

    def handle(self, *args, **options):
        #TECHNICAL ELECTIVE SUBJECTS: MATH, STA, COMPSCI, PHYSICS, CHEM, ECE, ME, ENERGYEGR, CEE
        #Hardcoded Technical URLS
        techurls = [
        "https://streamer.oit.duke.edu/curriculum/courses/subject/CHURHST%20-%20Church%20History?access_token="
        ]

        #Append GLOBAL TOKEN
        i = 0
        while i < len(techurls):
            techurls[i] = techurls[i]+TOKEN
            # logger.error(techurls[i])
            i += 1

        for url in techurls:
            r = requests.get(url)
            x = r.json()
            # logger.error(x)
            first_key = {}
            first_key = x['ssr_get_courses_resp']
            second_key = {}
            second_key = first_key['course_search_result']
            message = second_key['ssr_crs_gen_msg']

            #Key to check to determine if this entry should be skipped or not
            if message is not None:
                print("Request returned Null --> Exiting")
                exit()

            third_key = {}
            third_key = second_key['subjects
            fourth_key = {}
            fourth_key = third_key['subject']
            fifth_key = {}
            fifth_key = fourth_key['course_summaries']
            SUBJECT = fourth_key['subject']
            logger.error("SUBJECT IS: "+SUBJECT)
            mylist = fifth_key['course_summary']

            elective = "Approved Technical Elective"

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
            print("My dataset is:")
            print(dataset.export('csv'))
            self.stdout.write(self.style.SUCCESS('DATA WRANGLING SUCCESS'))

            # Import dataset into database
            course_resource = CourseResource()

        #DRY RUN of import
            result = course_resource.import_data(dataset, dry_run=True)
            if result.has_errors():
                self.stdout.write(self.style.ERROR('DRY RUN FAILED'))
                exit()
            else:
                self.stdout.write(self.style.SUCCESS('DRY RUN PASSED'))

        # Actual import
        #     true_import = course_resource.import_data(dataset, dry_run=False)
        #     if true_import.has_errors():
        #         self.stdout.write(self.style.ERROR('IMPORT FAILURE'))
        #         exit()
        #     else:
        #         self.stdout.write(self.style.SUCCESS('IMPORT SUCCESS'))
        #
        # self.stdout.write(self.style.SUCCESS('ALL API IMPORT UPDATES PASSED'))
