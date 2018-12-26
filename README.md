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
# Table of Contents
1.0 [How to Run](#how-to-run)

1.1 [Environment File Configuration](#environment-file-configuration)

2.0 [Functionalities](#functionalities)

2.1 [Functionalities: Students](#functionalities-students)

2.2 [Functionalities: Advisors](#functionalities-advisors)

2.3 [Functionalities: DGS](#functionalities-dgs)

2.4 [Functionalities: Administrators](#functionalities-administrators)

3.0 [Custom Admin Interface](#custom-admin-interface)

4.0 [Authentication](#authentication)

5.0 [General Setup](#general-setup)

5.1 [General Setup: Models](#general-setup-models)

5.2 [General Setup: Views](#general-setup-views)

5.3 [General Setup: Form Validation](#general-setup-form-validation)

6.0 [Management Commands](#management-commands)

7.0 [Asynchronous & Background Tasks](#asynchronous-background-tasks)

8.0 [Docker Setup](#docker-setup)

# How to Run
To successfully build the project users must:
1. Clone the repository, add and correctly configure an environment file (.env)
2. Run the following command when navigated to the parent directory containing the `docker-compose.yml` file

```
sudo docker compose up
```

# Environment File Configuration
The .env file contains environment variables different components in the Django project rely upon. By setting these variables in a .env
file, we maintain security and secrecy of certain variables so that everyone who clones this project or has access to this repository
does not these variable values. The following variables should be set in a .env file:
```
SECRET_KEY=
DEBUG=
TOKEN= 
SENDGRID_API_KEY= 
CLIENT_ID= 
CLIENT_SECRET= 
DOCKER_NAME= 
DOCKER_USER= 
DOCKER_PASSWORD= 
password= 

```

1. `SECRET_KEY`: This variable is the key in Django to secure signed data – it is vital you keep this secure, or 
attackers could use it to generate their own signed values
2. `DEBUG`: This variable sets whether or not the Django project should be in Debug mode or not. 
2. `TOKEN`: This variable should be set equal to a DUKE API key. These can obtained by any person affiliated with 
Duke that has a Duke NetID. This token allows the Django project to make API calls to Duke's Curriculum API, 
which are explained more later in the README. 
3. `SENDGRID_API_KEY`: This variable should be set with a SendGrid API Key. This can be obtained by registering for a SendGrid 
account and creating an API Key. This variable is used to allow the Django project to send emails through SendGrid. 
4. `CLIENT_ID`: This variable refers to the Client ID associated with a new app created in the Duke CoLab App Manager. This app
is used to allow for Duke users to authenticate in the web application with their Duke  NetID's through OAuth 2.0. Both the ID
and the Secret associated with the CoLab app are necessary to allow for authentication. More is explained on this in the Authentication
section. 
5. `CLIENT_SECRET`: This refers to the Secret associated with the application users must create in the Duke CoLab App Manager to 
allow users to authentication through OAuth 2.0. Please refer to the Authentication section for more details. 
6. `DOCKER_NAME`: This variable should be set with the name you want to use for your Postgres database. This variable is used by 
the `docker-compose.yml` file when building a container for the database,  as well as by the Django project to allow it to 
communicate with the database. 
7. `DOCKER_USER`: This variable refers to the Postgres database username you want to use. It is used by the Django project and 
`docker-compose.yml` file in the same ways DOCKER_NAME is used. 
8. `DOCKER_PASSWORD`: This variable is the password associated with the Postgres database username. Again, it is used by the Docker
project and `docker-compose.yml` file in the same ways DOCKER_NAME and DOCKER_USER are used.
9. `password`: This variable should be set with the password users want to use for their superuser account to login to 
Django's Admin Interface. When the project is built in Docker a superuser account is created with the value set for 'password' with 
the username 'superuser'. How this is implemented is explained more in the [Management Commands](#management-commands) section.

**Note:** Docker-compose expects .env variables to be typed as so:
```
key=value

```

Leave **no spaces** between the value and the equal sign.

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

# OAuth 2.0 Authentication
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

# General Setup
The Django project is titled 'programofstudy' and is setup with 5 different applications: meng, ms, phd, 
administration, and shared. Meng, ms, and phd handle urls, views, models, etc. for MEng, MS, and PhD program of 
study forms respectively. The shared app primarily contains templates and models that are utilized. by the majority 
of the other applications. For example, shared contains the Course and User models. The administration app contains 
views, urls, and templates for the custom admin interface.

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

# Management Commands
Django has a built in API to allow for developers to build their own admin.py management commands. These commands allow for the automation of 
certain administrative functions. Specifically, scripts can be written to automate the population of tables in the database. Custom management
commands were built to allow for the automatic population of data tables every time the web application was spun up in Docker. The following 
commands were built to populate our database initially so administrators did not have to do so manually. These commands are run in Docker 
when our `web` Docker container is spun up:
1. *addgroups.py*: This command creates distinct Groups for students, advisors, administrators, and DGS accounts. Each Group is then
given a subset of different permissions that allows each Group to have access to a different set of functions in the web application.
The command finally adds these Groups to the Groups table in the database.
2. *coursetypes.py*: This commands adds the two types of Course Categories used in the web application to the Course Type table:
a) Elective b) Technical Elective. This command automates adding these two data rows to the Course Type table.
3. *firstuser.py*: This command automates the creation of a superuser command that is used to login to the Django Admin Interface. It makes 
use of the `password` environment variable to set the password of the superuser account. The username is set as **superuser**. 
4. *590courses.py*" This command automates the creation of ECE 590 Special Topics courses in the databaes. Every year the ECE department creates Special
Topics courses that are not always consistently offered. These courses are listed under ECE 590. These courses are not found in the Duke Curriculum
API so they must be manually added to the database. In order to avoid that, the above management command was created to automate the process of
creating Special Topics Courses in the database.

The following commands were built to automate imports of Course data into the Course Table. These functions were used in conjunction with Celery
to be ran in the background. More information on Celery is located in [Asynchronous & Background Tasks](#asynchronous-background-tasks).
1. *importechnical.py*: This command automates the import of Technical Elective Courses from the Duke Course Curriculum API.
2. *importelective.py*: This command automates the import of Elective Courses from the Duke Course Curriculum API. 
3. *updatelective.py*: This command automates the update of Elective Courses from the Duke Course Curriculum API.
4. *updatetechnical.py*: This command automes the update of Technical Elective Courses from the Duke Course Curriculum API.

The following commands were built to send emails to multiple DGS and Advisor accounts. These commands were used in conjuction with Celery to be ran
in the background. More information on Celery is located in [Asynchronous & Background Tasks](#asynchronous-background-tasks).
1. *dgsemail.py*: This command emails DGS accounts the number of Program of Study forms that are pending review.
2. *email.py*: This command emails Advisor accounts the number of Program of Study forms that are pending review. 

# Asynchronous & Background Tasks
Some functionalities, such as the mass import of Courses into the database through the Custom Admin Interface, take more than 
a few seconds to accomplish. As a result, if users attempt to run these functions, the user would normally have to wait a few minutes for the 
function to finish. The Gunicorn server that is used to run this web application times out if any request takes longer than 30 seconds. As a result,
functionalities built in this manner would fail. To allow for functions with long run times to work, we must run them asynchronously. This would mean
allowing a user to initiate a task to run in the background, allow a user to navigate to other parts of the web application while the task runs,
and finally be notified in some manner that the background task has finished. This workflow is accomplished through the Django Celery library.

Celery is a library that allows developers to make use of task queues. Task queues are  used as a mechanism to distribute work across threads or machines.
A task queue’s input is a unit of work called a task. Dedicated worker processes constantly monitor task queues for new work to perform. Through Celery,
any task can be allowed on the task queue, and worker processes will be notified of their presence in the queue, perform these tasks asynchronously.
Celery communicates via messages, usually using a broker to mediate between clients and workers.  To initiate a task the client adds a message to 
the queue, the broker then delivers that message to a worker. In our setup, Redis was used as the message broker to notify worker processes of new 
tasks. Celery was used to allow time intensive requests to run in the background. In particular, it was used to process:
1. Course Imports made from Duke Curriculum API calls
2. Send scheduled emails to Advisor and DGS accounts

# Docker Setup
The web application makes use of Docker and is built through docker-compose. Each command in the Dockerfile used to
build our own custom image is explained below:
1. `FROM python:3.5`: Sets up base project set-up to install all the dependencies 
to run your application Python as our base since Django is a Python project.
2. `ENV PYTHONUNBUFFERED 1`: Creates an environment variable and passes and standard output
to be printed to the Terminal. 
3. `RUN mkdir /code`: Creates a directory within the container.
4. `WORKDIR /code`: Specifies a new default directory within the Docker image's file system.
5. `ADD requirements.txt /code/`: Adds requirements.txt file to /code directory
6. `RUN pip3 install -r requirements.txt`: installs requirement files that are needed to run the Django project.
7. `ADD . /code/`: Copys all project files in current directory into /code directory. These project files are necessary for each container
that is built using this Dockerfile as explained later. 
8. `RUN groupadd posgroup`: Creates a new Group Account on the host Linux OS
9. `RUN useradd -m -G posgroup posuser`: Creates a new user "posuser" to the newly created Group Account.
10. `RUN mkdir /var/run/celery`: Creates a new directory
11. `RUN chown -R posuser:posgroup /var/run/celery/`: Makes the newly created directory owned by the
newly created Group Account.
12. `RUN chown -R posuser:posgroup /code/`: Makes the new Group own the /code directory and all of its subfiles. 
13. `USER posuser`: Sets the current user running this container as "posuser". This makes sure that the container
is not running with root privileges. We gave permissions to the Group this User is a part of to the folder "/var/run/celery" as 
the user running the container based off this image needs access to this directory to correctly run Celery tasks. The containers
used for Celery are explained in greater detail later in this section.

This above image is used in multiple containers as shown in the `docker-compose.yml` file below: 
```version: '3'
services:
 db:
   image: postgres
   environment:
     - POSTGRES_USER=${DOCKER_USER}
     - POSTGRES_PASSWORD=${DOCKER_PASSWORD}
     - POSTGRES_DB=${DOCKER_NAME}
 redis:
   image: "redis:alpine"
 web:
   build: .
   command: bash -c "python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py addgroups && python3 manage.py coursetypes && python3 manage.py firstuser && gunicorn programofstudy.wsgi -b [::]:8000"
   volumes:
     - .:/code
   ports:
     - "8000:8000"
   depends_on:
     - db
     - redis
 celery:
   build: .
   command: celery -A programofstudy worker -l info
   volumes:
     - .:/code
   depends_on:
     - db
     - redis
   expose:
     - "8000"
 celerybeat:
   build: .
   command: celery -A programofstudy beat -l info --pidfile="/var/run/celery/celerybeat.pid" --schedule="/var/run/celery/celerybeat-schedule"
   volumes:
     - .:/code
   depends_on:
     - db
```

This `docker-compose.yml` file is used to define multiple services that are needed to be running in order to allow the entire 
application to function correctly. The first two services: db and redis use images downloaded from Docker Hub.
The following descriptions summarize what each service does and how each service was configured:
1. `db`: This service contains the Postgres database utilized by the web application. It makes use of variables set in our 
.env file through the environment option to correctly configure the Postgres database name, user and password.
2. `redis`: This service is used as the message broker for the celery and celerybeat services explained later. As explained in 
the [Asynchronous & Background Tasks](#asynchronous-background-tasks) section Celery makes use of a message broker to feed messages
between workers and clients. This service is used to act as the message broker for Celery in this web application.

The next 3 services: web, celery, and celerybeat are built using the Dockerfile specified above. In all three we specify to build
each container using the Dockerfile above by feeding '.' to the build docker-compose configuration line. This specifies that the
Dockerfile to use to build this service is within our current directory. In each service we also mount the current directory to
the /code directory. In our Dockerfile we created a /code directory and copied all of the project files in our current directory to 
the /code directory as shown above. Here we are now mounting our current directory as a data volume in each of the 3 services. This
step allows any changes that are made to the project directory to be reflected in each container's /code directory. This means that
any changes to files within the current directory will also change matching files in the /code directory since the /code directory
contains a copy of each file in the current directory.

3. `web`: This service runs the Django project in the web application. When the container is started the lines specified
in "command" are run. The commands that are run a) create database migrations b) migrate those migrations to the database c) 
run multiple Django management commands and d) deploy the Django project on a Gunicorn web server to begin accepting web connections.
The management commands are explained in greater detail in [Management Commands](#management-commands). The management commands 
that are run when this container starts add permission groups, populate the Course Type table, and create a superuser account 
if it does not already exist. 
4. `celery`: This service runs Celery worker processes. As explained in [Asynchronous & Background Tasks](#asynchronous-background-tasks)
Celery is a task queue. Celery worker processes wait to be delivered a message from our message broker, Redis, when it detects a task
is in the queue. This container waits to be sent messages from Redis and will then run the associated tasks asynchronously and in
the background. This allows users to navigate to different web pages after initiating a certain task. For example, any task related
to import Courses from the Duke API run asynchronously due to this service. It makes use of the project files in the /code directory to
run celery tasks correctly.
5. `celery-beat`: This service runs a Celery beat, a scheduler. Certain tasks, such as emailing DGS and Adviser accounts, are configured
in Celery in the Django project to run at a scheduled time every day. Celery beat is the scheduler that sets the exact time at which
emails are sent out to DGS and Advissor accounts. This service is responsible for allocating scheduled tasks on the task queue.
When these tasks are within the queue, Redis will detect them and send a message to the `celery` service which will run the task
asynchronously. It makes use of the project files in the /code directory to schedule celery tasks correctly.




