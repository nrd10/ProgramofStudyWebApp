# Program Of Study Web Application
The purpose of this project is to allow Duke Electrical & Computer Engineering graduate students (MEng, MS, PhD) to easily submit program of study forms. The web application will also allow for the easy review (acceptance or rejection) of these forms by advisor and Duke Graduate School (DGS) accounts.

# Code Organzation
The Django project is titled 'programofstudy' and is setup with 5 different applications: meng, ms, phd, administration, and shared. Meng, ms, and phd handle urls, views, models, etc. for MEng, MS, and PhD program of study forms respectively. The shared app primarily contains templates and models that are utilized. by the majority of the other applications. For example, shared contains the Course and User models. The administration app contains views, urls, and templates for the custom admin interface.

# General Setup: Models
The models in the shared app are used as Foreign Keys or ManytoManyFields in the models im the meng, ms, and phd applications. These models are User (a custom User model), Course, Concentration, and Course Type. The Course Type model stores two values, Elective and Technical Elective. Each course is classified as one or the other or both. The Concentration model stores the 6 possible ECE concentrations.

The models in the meng application are MEngPOS and MEngComment. The MEngPOS model stores program of study forms geared towards ECE MEng students. The MEngComment model stores comments that advisors and DGS administrators may write for a program of study form.

The models in the ms application are MSCoursePOS, MSCourseComment, MSProjectPOS, MSProjectComment, MSThesisPOS, and MSThesisComment. There are 3 types of program of study forms ECE MS students depending on if their Master of Science degree is Coursework-based, Project-based or Thesis-based. The models mentioned above store program of study forms for each type of degree. The models ending with "Comment" store comments left by advisors and DGS administrators for particular program of study forms.

The models in the phd application are CurricularArea, PHDBachelorPOS, PHDBachelorComment, PHDMasterPOS, and PHDMasterComment. The CurricularArea model stores teh four possible Curricular Areas that ECE PhD students may focus on in Duke's ECE curriculum. There are two types of forms Duke ECE PhD students may submit, one for if they are matriculating with just a bachelor's degree, and one if they are matriculating with a master's degree. The two models ending in "POS" store forms for each type of form. The models ending in "Comment" store comments left by advisors and DGS administrators for program of study forms for each type of form.

# General Setup: User Account Types/Permissions
There are different types of users that can use the web application. There are Student accounts, Advisor accounts, DGS accounts, and Administrator accounts. The type of an account a user has is chosen through the MultiSelectField "user_type" in the custom User model. A Student account can either be "MEng", "MS", or "PhD". An Advisor, Administrator or DGS account can also be one of the other two types of accounts. So an Advisor account may also be a DGS account. Each user account type has a different set of permissions that changes the functions and web pages available to them in the web application. So for example, Advisor and DGS accounts cannot submit forms but they can approve and reject forms. Student accounts can create new program of study forms, but are unable to approve or reject forms.

# General Setup: Views
The meng, ms, and phd applications each have a repeated set of class-based and function-based views. For each type of program of study form, there is a view to create a new form (CreateView) , update an existing form (UpdateView), list out all (ListView), show the details of an existing form (DetailView), approve a form, reject a form, and search for a specific type of form. Some of these class-based or function-based views are repeated for Advisor and DGS accounts. For example, the Advisor accounts have access to a view (ListView) that allows them to see all submitted program of study forms for students who they advise.

# General Setup: Search
The meng, ms, and phd application each make use of Django's filters API to allow DGS and administrator accounts to easily find program of study forms for each type of student.

# General Setup: Forms
The meng, ms, and phd applications all make use of ModelForms located in forms.py for each application. Students can view, fill out and submit these forms to represent their program of study. The Django Select2 library was used to allow students to easily search and select courses for each field in each distinct model. Validation was added to these student program of study forms to meet specific constraints outlined by the Duke ECE department. Specifically, courses are not counted for more than one field, and  no more than 2 Independent Study courses can be used towards a student's program of study.

# Database Configuration
We used a Postgresql database to store data models
