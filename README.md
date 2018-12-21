# Program Of Study Web Application
This Django based web application was built to be used to streamline the submission of ECE Program of Study forms. 
All matriculating Duke graduate students, both Masters and PhD students, are required to fill out a departmental Program of 
Study form before enrollment. The department uses this form to gain a sense of what courses each student plans on taking 
during their time at Duke. Once students fill out the form, they must send it to their designated departmental advisor. 
The advisor rejects or approves the schedule and on approval submits it to the Director of Graduate Studies for approval. 
The approval process currently is done on paper, posing an issue for the department to keep track of each individual form 
for each student. Additionally, the department has to manage sending forms back and forth from advisors to students in 
person or over email when forms are rejected or approved. This application automates the entire process of creating 
forms, approving or rejecting forms, and tracking any changes related to a student’s planned course of study.
# How to Run
The project is set up with Docker. After cloning the repository run:

```
sudo docker compose build
sudo docker compose up
```
# Functionalities
The web application, as stated above, handles the creation, submission, and 
review of Program of Study forms for Duke ECE graduate students. 
The application handles 4 different user types: Student accounts, Advisor accounts, DGS accounts, 
and Adminstrator accounts. Each user account 
type has a different set of permissions that changes the functions and web pages available to them 
in the web application. For example, Advisor and DGS accounts cannot submit forms but they can 
approve and reject forms. Student accounts can create new program of study forms, but are unable 
to approve or reject forms. The separate set of features available to each user type is explained below.
# Functionalities: Students
Functions available to students are summarized below:
1. **Create and submit a Program of Study form**
2. **View all forms the student has ever submitted**, organized by whether the forms were Approved, Rejected, or Pending approval
3. **Receive notifcations by email** when a form is Approved or Rejected

A Student account can  either be "MEng", "MS", or "PhD" corresponding to MEng, MS, and PhD graduate students, respectively.
Students accounts are separated into those three categories since each student has separate types of the Program of Study form 
since the requirements for each degree differ. Each student is able to create and submit Program of Study forms through the application.
The application's PostgresSQL database can be populated by all of Duke's courses, allowing for the submission of forms populated
with courses each student plans on enrolling in in their time at Duke. The Django Select2 
library was used to allow students to easily search and select courses for each field in the Program of Study form.
After submitting completed forms, students will receive email notifications when a form is either approved or rejected. 
Students also have access to a ListView that shows all forms each student has ever submitted organized by whether the form 
is Approved, Rejected, or Pending Review. Students may also edit their submitted forms and resubmit them as long as the form 
is not waiting to be Approved or Rejected by an Advisor or a DGS account.


#### The image below shows an example of the form creation page accessible by students:
![Form_Creation](/uploads/e41eb9390c19138ebcfea37f2930c349/Form_Creation.png) 


# Functionalities: Advisors
Functions available to advisors are summarized below:
1. Advisors can **view submitted Program of Study forms for student's who are marked as their Advisees**
2. Advisors can **Reject or Approve forms** for their advisees
3. Advisors can **leave comments** justifying why they rejected students in order to inform students why their form was rejected
4. Advisors will **receive email notifications** of the number of submitted Program of Study forms that are awaiting their review

Advisor accounts have access to features allowing them to review submitted Program of Study forms. Each student account, when created
is assigned an Advisor. When a student submits a Program of Study form, their assigned Advisor will gain access to the submitted 
form and have the ability to Approve or Reject the form. Advisors are able to view, approve, and reject Program of Study forms for any of their Advisees
(student accounts associated with that Advisor). Once Program of Study forms are Approved by an Advisor, they are viewable by DGS accounts 
who then must approve them. If they are rejected, student's must resubmit an amended Program of Study form. 

#### The image below shows the view an Advisor receives when viewing a submitted POS Form: 
![Advisor_View](/uploads/56f9f03ac1ed5e54228aa1f63542b12a/Advisor_View.png)

# Functionalities: DGS
Functions available to advisors are summarized below:
1. DGS accounts can **view submitted Program of Study forms for all Program of Study forms approved by an Advisor**
2. DGS accounts can **Reject or Approve forms** already approved by an Advissor
3. DGS accounts can **leave comments** justifying why they rejected students in order to inform students why their form was rejected
4. DGS accounts will **receive email notifications** of the number of Advisor approved Program of Study forms that are awaiting their review

DGS accounts have access to features allowing them to review all Program of Study forms Approved by an Advisor. 
Once Program of Study forms are Approved by an Advisor, they are viewable by DGS accounts.
If forms are rejected by a DGS account, student's must resubmit an amended Program of Study form. 

#### The image below shows the view a DGS account receives when viewing a submitted POS Form:
![DGS_Form_View](/uploads/3a625a9f35816c934d61310cfb33ba4f/DGS_Form_View.png)



#### The image below shows the view a DGS account will view when searching for previously reviewed forms:
![DGS_Form_Search](/uploads/30c0a3a5af570f199a033809603923bb/DGS_Form_Search.png)


# Functionalities: Administrators
Functions available to Administrators are summarized below:
1. Administrators can **access all of the features in the Custom Admin Interface**

Django's built in Admin Interface requires knowledge on how Django models were built. Since no administrators in Duke's ECE department helped 
build this application, it would be tough for any administrators to be comfortable populating and editing data models through the Admin Interface.
As a result, we built a Custom Admin Interface that requires less knowledge about the underlying data tables in the database on the part of administrators.
This new interface allows users the same functionalities as the Django Admin Interface. Administrators can search, delete and create new data entries in
almost all of the data tables without having to actually know the names and structure of each data table. Additional features were also added to the 
Custom Admin Inteface to expedite the process of creating new users and importing data into data tables. The features of the interface are 
explained in the section below.

# Custom Admin Interface
Administrators can do the following things through the Custom Admin Interface:
1. **Search for Users, Courses, and all types of Program of Study forms** stored in the database
2. **Delete Users, Courses and all types of Program of Study forms** stored in the database 
2. **Create individual new Courses** in the database
3. **Create new Users individually** in the database. Administrators should create users in this fashion as the User Creation page in the Custom
Admin Interface requires a NetID to be entered when registering a user but not a password. This is desired as users will be authenticating
with their Duke credentials and the database will not be storing their Duke password. 
4. **Create new Users through an uploaded CSV file**. This feature allows an administrator to upload a CSV file with each row having
values for the following columns in order:Student ID, Last Name, First Name, Email, NetID, Academic Plan (type of student), and Advisor. 
This features allows administrators to avoid having to individually create a new user for all students in a class. 
After users Submit the CSV file, the users in the CSV file will be uploaded into the web application's database. An example
CSV file is within the repository and named **ExampleNETIDStudentSpreadsheet.csv**.
5. **Import all of Duke's offered Courses through Duke's Curriculum API**. Any Duke University user with Duke credentials can create an API Key for 
Duke's API Catalog. After creating one and setting a parameter in the .env file accessible by the Docker container running this project, 
the web application is able to make requests to the API for Duke's course listings. This function makes calls to that API to import all of 
Duke's courses. Due to the fact that the import is not instantaneous and the fact that the Gunicorn WGSI server running in the Docker container 
times out after a minute passess in any request, this function must run asynchronously. This web application makes use of the Celery project with
built in Django support that supports asynchronous tasks. Through Celery, this Course import can run in the background and allow users to navigate
to other sections of the web application as courses continue to be imported. How asynchronous tasks are built in this application is explained 
more in the Asynchronous Tasks section.
6. **Update all of Duke's offered Courses through Duke's Curriculum API**. This function works similarly to the full Course import function in that
it makes use of Duke's API Catalog to import courses. This function should be run when the Course table in the Postgres database is already fully updated.
This function updates the Courses within the database. It checks if a Course listing had it's name changed and will update the name of the course for 
all courses in Duke's Course Catalog. Additionally, if any new Courses are offered in one semester, it will import those Courses into the database if 
they are not already in the web application's Course table. **Note**: This function **updates Courses by their listing**. If a Course's listing changes, but
retains the same name, the database will import the new Course listing and will retain the old Course listing. This means that two different Course listings
with the same name will be within the web application's database. Administrators should run this function every semester to update the Course table within
the database with new Course listings that are offered by Duke.
7. **Delete all Courses** in the database. This functionality makes it easier to completely erase all of the Courses currently in the database. 
8. Create a Program of Study form **on behalf of a student**. This functionality allows Administrators to submit a Program of Study form for a student.
This may be necessary if a student decides to have a unique set of Courses that they would like to take that does not abide by the normal form validation
procedure. For example, if a student wants a concentration course to count as both an Elective and a Concentration Course, this will not be possible
if a student submits a Program of Study form as Courses cannot count twice. If after discussing with the DGS or an Advisor that this is okay, an Administrator
can submit the form for the student. These submission functionalities do not have the same Form Validation as the student submisssion functionalities. This
allows the Administrator account greater freedom in submitting a Program of Study form. 

# Authentication
The web application makes use of of the OAuth 2.0 authentication protocol rather than Django's built in login system. The authentication framework
is utilized as it is an industry standard authentication protocol, and to allow users of the web application to authenticate with their Duke credentials.
Administrators must first register new users through the application's Custom Admin Interface. When creating a new user, administrators must
associate a Duke netID with each user. After creating a new user in the database, these users will be recognized by the application and will then
be able to login using their Duke netID and Duke password. 

The authentication protocol was integrated into the web application with assistance from 
[this tutorial](https://gist.github.com/billhanyu/788358f01eea969b6d1dfd9fb0d87750).

After registering an App in the Duke CoLab App Manger as mentioned in step 1 of the above tutorial, when users click the Login button on the main page, 
they are redirected to the correct URL with the specified parameters as in step 2 of the above tutorial. **Note**: A Client ID and Client Secret were 
taken from the App that was registered in step 1. These parameters are specified in the .env file specified above, that is accessible by the 
Docker container. To get OAuth 2.0 to work in Django, in step 2 the user is redirected to a middle webpage which is able to catch the Access Token 
returned by the redirect URL. After the middle webpage catches the token, it immediately makes it request to Duke's OAuth sever with the access token
to correctly authenticate the user. In this project, the view that initiates the initial redirect request is: **duke_login** found 
in *administration.views.py*. The view handling the middle webpage to correctly retrieve the Access Token is **middle_request** found in
*shared.views.py*. The view that handles the final step in authenticating, sending a GET request with the Access Token, is 
**OIT_login** found in *shared.views.py*.

# Code Organzation
The Django project is titled 'programofstudy' and is setup with 5 different applications: meng, ms, phd, 
administration, and shared. Meng, ms, and phd handle urls, views, models, etc. for MEng, MS, and PhD program of 
study forms respectively. The shared app primarily contains templates and models that are utilized. by the majority 
of the other applications. For example, shared contains the Course and User models. The administration app contains 
views, urls, and templates for the custom admin interface.

# General Setup: Environment File

# General Setup: Models
The models in the shared app are used as Foreign Keys or ManytoManyFields in the models im the meng, ms, and phd applications. 
These models are User (a custom User model), Course, Concentration, and Course Type. The Course Type model stores two values, 
Elective and Technical Elective. Each course is classified as one or the other or both. The Concentration model stores the 6 
possible ECE concentrations.

The models in the meng application are MEngPOS and MEngComment. The MEngPOS model stores program of study forms geared 
towards ECE MEng students. The MEngComment model stores comments that advisors and DGS administrators may write for a 
program of study form.

The models in the ms application are MSCoursePOS, MSCourseComment, MSProjectPOS, MSProjectComment, MSThesisPOS, and 
MSThesisComment. There are 3 types of program of study forms ECE MS students depending on if their Master of Science 
degree is Coursework-based, Project-based or Thesis-based. The models mentioned above store program of study forms 
for each type of degree. The models ending with "Comment" store comments left by advisors and DGS administrators 
for particular program of study forms.

The models in the phd application are CurricularArea, PHDBachelorPOS, PHDBachelorComment, PHDMasterPOS, and 
PHDMasterComment. The CurricularArea model stores teh four possible Curricular Areas that ECE PhD students may 
focus on in Duke's ECE curriculum. There are two types of forms Duke ECE PhD students may submit, one for if 
they are matriculating with just a bachelor's degree, and one if they are matriculating with a master's degree. 
The two models ending in "POS" store forms for each type of form. The models ending in "Comment" store comments 
left by advisors and DGS administrators for program of study forms for each type of form.


# General Setup: Views
The meng, ms, and phd applications each have a repeated set of class-based and function-based views. 
For each type of program of study form, there is a view to create a new form (CreateView) , update an 
existing form (UpdateView), list out all (ListView), show the details of an existing form (DetailView), 
approve a form, reject a form, and search for a specific type of form. Some of these class-based or 
function-based views are repeated for Advisor and DGS accounts. For example, the Advisor accounts have 
access to a view (ListView) that allows them to see all submitted program of study forms for students who they advise.

# General Setup: Form Validation
Each Program of Study form was validated to abide by the following constraints:
1. Courses could **not be counted more than one time** in any Program of Study form
2. ECE 899: Independent Study courses could **count only 2x towards a degree**
3. Undergraduate courses with listings below 500 count **count only 2x towards a degree**
4. Multiple Independent Studies and Undergrdaute courses would **count as only 2 courses in a degree**
The meng, ms, and phd applications all make use of ModelForms located in forms.py for each application. 
Students can view, fill out and submit these forms to represent their program of study. 
Validation was added to these student program of study forms to meet specific constraints outlined by the 
Duke ECE department. Specifically, courses are not counted for more than one field, and  no more than 2 
Independent Study courses can be used towards a student's program of study.
# General Setup: Management Commands

# Asynchronous Tasks

# Docker Setup
The web application makes use of Docker and is built through docker-compose. Each command in the Dockerfile is
explained below:
1. "FROM python:3.5": Sets up base project set-up to install all the dependencies 
to run your application Python as our base since Django is a Python project.
2. "ENV PYTHONUNBUFFERED 1": Creates an environment variable and passes and standard output
to be printed to the Terminal. 
3. "RUN mkdir /code": Creates a directory within the container.
4. "WORKDIR /code": Specifies a new default directory within the Docker image's file system.
5. "ADD requirements.txt /code/": Adds requirements.txt file to /code directory
6. "RUN pip3 install -r requirements.txt": installs requirement files that are needed to run the Django project.
7. "ADD . /code/": Copys all project files in current directory into /code directory.
8. "RUN groupadd posgroup": Creates a new Group Account on the host Linux OS
9. "RUN useradd -m -G posgroup posuser": Creates a new user "posuser" to the newly created Group Account.
10. "RUN mkdir /var/run/celery": Creates a new directory
11. "RUN chown -R posuser:posgroup /var/run/celery/": Makes the newly created directory owned by the
newly created Group Account.
12. USER posuser: Sets the current user running this container as "posuser". This makes sure that the container
is not running with root privileges. 

