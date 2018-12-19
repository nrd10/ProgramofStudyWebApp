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

# Custom Admin Interface

# Code Organzation
The Django project is titled 'programofstudy' and is setup with 5 different applications: meng, ms, phd, 
administration, and shared. Meng, ms, and phd handle urls, views, models, etc. for MEng, MS, and PhD program of 
study forms respectively. The shared app primarily contains templates and models that are utilized. by the majority 
of the other applications. For example, shared contains the Course and User models. The administration app contains 
views, urls, and templates for the custom admin interface.

# Authentication

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

# Search
The meng, ms, and phd application each make use of Django's filters API to allow DGS and administrator 
accounts to easily find program of study forms for each type of student.

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

