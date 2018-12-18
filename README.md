# Program Of Study Web Application
This Django based web application was built to be used to streamline the submission of ECE Program of Study forms. All matriculating Duke graduate students, both Masters and PhD students, are required to fill out a departmental Program of Study form before enrollment. The department uses this form to gain a sense of what courses each student plans on taking during their time at Duke. Once students fill out the form, they must send it to their designated departmental advisor. The advisor rejects or approves the schedule and on approval submits it to the Director of Graduate Studies for approval. The approval process currently is done on paper, posing an issue for the department to keep track of each individual form for each student. Additionally, the department has to manage sending forms back and forth from advisors to students in person or over email when forms are rejected or approved. This application automates the entire process of creating forms, approving or rejecting forms, and tracking any changes related to a student’s planned course of study.
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
A Student account can  either be "MEng", "MS", or "PhD" corresponding to MEng, MS, and PhD graduate students, respectively.
Each student is able to create and submit Program of Study forms through the application. Students accounts are separated into
those three categories since each student has separate types of the Program of Study form since the requirements for each degree differ.
The application's database can be populated by all of Duke's courses, allowing for the submission of forms populated
with courses each student plans on enrolling in in their time at Duke. The Django Select2 
library was used to allow students to easily search and select courses for each field in the Program of Study form.
After submitting completed forms, students will receive email notifications when a form is either approved or rejected. 
Students also have access to a ListView that shows all forms each student has ever submitted organized by whether the form 
is Approved, Rejected, or Pending Review.


The screenshot below shows an example of the form creation page accessible by students:
![Form_Creation](/uploads/e41eb9390c19138ebcfea37f2930c349/Form_Creation.png) 

# Functionalities: Advisors

# Functionalities: DGS

# Functionalities: Administrators

# Custom Admin Interface

# Code Organzation
The Django project is titled 'programofstudy' and is setup with 5 different applications: meng, ms, phd, 
administration, and shared. Meng, ms, and phd handle urls, views, models, etc. for MEng, MS, and PhD program of 
study forms respectively. The shared app primarily contains templates and models that are utilized. by the majority 
of the other applications. For example, shared contains the Course and User models. The administration app contains 
views, urls, and templates for the custom admin interface.

# Database Configuration
We used a Postgresql database to store data models

# Authentication

# Models
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

# Search
The meng, ms, and phd application each make use of Django's filters API to allow DGS and administrator 
accounts to easily find program of study forms for each type of student.

# Forms
The meng, ms, and phd applications all make use of ModelForms located in forms.py for each application. 
Students can view, fill out and submit these forms to represent their program of study. The Django Select2 
library was used to allow students to easily search and select courses for each field in each distinct model. 
Validation was added to these student program of study forms to meet specific constraints outlined by the 
Duke ECE department. Specifically, courses are not counted for more than one field, and  no more than 2 
Independent Study courses can be used towards a student's program of study.

