from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.forms.utils import ErrorList
from ms.models import *
from shared.models import *
from meng.models import *
from phd.models import *
from django import forms
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.management import call_command
from administration.filters import *
from administration.forms import *
from django.contrib.auth.models import Group
from import_export import resources
from administration.resources import UserResource
from django.db.models import Q
from django.conf import settings
from tablib import Dataset
from decouple import config
from .tasks import populate_database, update_database
logger = logging.getLogger('administration/views.py')

import sys
import tablib
import xlwt

#Serves template that gives Form Creation Options
@permission_required('meng.MEng_Admin_Create')
@permission_required('ms.MSc_Admin_Create')
@permission_required('ms.MSp_Admin_Create')
@permission_required('ms.MSt_Admin_Create')
@permission_required('phd.PHDBS_Admin_Create')
@permission_required('phd.PHDMS_Admin_Create')
def admincreate(request):
    """
    Create function for admin
    """
    return render(
        request,
        'formoptions.html',
    )


#Serves template that gives Database Options
@permission_required('meng.MEng_Admin_View')
@permission_required('ms.MSc_Admin_View')
@permission_required('ms.MSp_Admin_View')
@permission_required('ms.MSt_Admin_View')
@permission_required('phd.PHDBS_Admin_View')
@permission_required('phd.PHDMS_Admin_View')
def admindatabase(request):
    """
    Create function for admin
    """
    return render(
        request,
        'databaseoptions.html',
    )

#Runs Custom Commands to Import Courses to Database
@permission_required('shared.Course_Admin_Create')
def populatedb(request):
    #Import Technical Electives
    try:
        # call_command('importechnical')
        # # Add Concentrations
        # call_command('addconcentration')
        # # Import Electives
        # call_command('importelective')
        netid = request.user.netid
        populate_database.delay(netid)

        messages.add_message(request, messages.INFO, "Course Import In Progress")
        return redirect('admin-database')

    except:
        messages.add_message(request, messages.ERROR, "The Database Did Not Import Courses Correctly!")
        e = sys.exc_info()[0]
        logger.error(e)
        return redirect('admin-database')


#Runs Custom Commands to Update Database
@permission_required('shared.Course_Admin_Create')
def updatedb(request):
    #Update Technical Electives
    try:
        # call_command('updatetechnical')
        # #Update Electives
        # call_command('updatelective')
        netid = request.user.netid
        update_database.delay(netid)
        messages.add_message(request, messages.INFO, "Course Update In Progress")
        return redirect('admin-database')

    except:
        messages.add_message(request, messages.ERROR, "The Database Did Not Update Correctly!")
        e = sys.exc_info()[0]
        logger.error(e)
        return redirect('admin-database')



@permission_required('shared.Course_Admin_Create')
def CourseSearch(request):
    posfilter = CourseFilter(request.GET, queryset=Course.objects.all())
    pos_list = posfilter.qs
    page = request.GET.get('page', 1)
    #Pagination by 5
    paginator = Paginator(pos_list, 250)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    args = {'filter':posfilter,'users':users, 'page':page, 'search':'custom_listing',}
    # return render(request, 'search.html', {'filter': posfilter})
    return render(request, 'coursesearch.html', args)


class CourseDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'shared.Course_Admin_Create'
    model = Course
    template_name = 'course_detail.html'

class CourseUpdateView(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    permission_required = 'shared.Course_Admin_Create'
    model = Course
    form_class = CourseForm
    template_name_suffix = '_course_form'

class CourseCreateView(PermissionRequiredMixin, LoginRequiredMixin, generic.CreateView):
    permission_required = 'shared.Course_Admin_Create'
    model = Course
    form_class = CourseForm
    template_name_suffix = '_course_form'


#Admin Function to Delete 1 Course
@permission_required('shared.Course_Admin_Create')
def coursedelete(request, form_id):
    form = get_object_or_404(Course, pk=form_id)
    form.delete()
    return redirect('admin-courses')


#Admin Function To Delete All Courses
@permission_required('shared.Course_Admin_Create')
def fullcoursedelete(request):
    try:
        all = Course.objects.all()
        all.delete()
        messages.add_message(request, messages.SUCCESS, "Full Course Delete Success!")
        return redirect('admin-database')
    except:
        messages.add_message(request, messages.ERROR, "The Database did not Delete Courses correctly!")
        return redirect('admin-database')


class UserCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'shared.User_Admin_Create'
    model = User
    form_class = UserForm
    template_name_suffix = '_user_form'

    def form_valid(self, form):
        Advisor = Group.objects.get(name="Advisor_group")
        DGS = Group.objects.get(name="DGS_group")
        Admin = Group.objects.get(name="Administrators")
        Meng = Group.objects.get(name="MEng_students")
        MS = Group.objects.get(name="MS_students")
        PhD = Group.objects.get(name="PHD_students")

        types = form.instance.user_type

        # logger.error("My user is:")
        # logger.error(form.instance)

        #Booleans to check for student and professor privileges
        Meng_bool = False
        MS_bool = False
        PhD_bool = False
        Advisor_bool = False
        Admin_bool = False
        DGS_bool = False
        student = False
        professor = False

        #Checks to set booleans to later add user to groups
        if ("MEng" in types):
            Meng_bool = True
            student = True
            logger.error("Meng is TRUE")
        if ("MS" in types):
            MS_bool = True
            student = True
            logger.error("MS is TRUE")
        if ("PhD" in types):
            PhD_bool = True
            student = True
            logger.error("PhD is TRUE")
        if ("Advisor" in types):
            Advisor_bool = True
            professor = True
            logger.error("Advisor is TRUE")
        if ("DGS" in types):
            DGS_bool = True
            professor = True
            logger.error("DGS is TRUE")
        if ("Administrator" in types):
            Admin_bool = True
            professor = True
            logger.error("Admin is TRUE")

        #Checks that user does not have student and professor privileges
        if ((student == True)&(professor == True)):
            messages.add_message(self.request, messages.ERROR, "Accounts may not have student privileges along with " \
            "DGS, Advisor, or Administrator privileges.")
            return redirect('admin-user-create')

        #Make Account Active
        form.instance.is_active = True

        #Save Form to Allow New User to be Added to Correct Group
        self.object = form.save()
        #Add user to correct groups
        if Meng_bool:
            Meng.user_set.add(form.instance)
        if MS_bool:
            MS.user_set.add(form.instance)
        if PhD_bool:
            PhD.user_set.add(form.instance)
        if Advisor_bool:
            Advisor.user_set.add(form.instance)
        if DGS_bool:
            DGS.user_set.add(form.instance)
        if Admin_bool:
            Admin.user_set.add(form.instance)

        logger.error("User groups are:")
        logger.error(form.instance.groups.all())

        #Set Account as Active

        #Redirect request to Success URL
        return HttpResponseRedirect(self.get_success_url())

class UserDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'shared.User_Admin_Create'
    model = User
    template_name = 'user_detail.html'

@permission_required('shared.User_Admin_Create')
def usercontrols(request):
    return render(
        request,
        'useroptions.html',
    )

@permission_required('shared.User_Admin_Create')
def searchoptions(request):
    return render(
        request,
        'searchoptions.html',
    )

#Allows DGS to search for forms: HISTORY PAGE
@permission_required('shared.User_Admin_Create')
def UserSearch(request):
    posfilter = UserFilter(request.GET, queryset=User.objects.all())
    pos_list = posfilter.qs
    page = request.GET.get('page', 1)
    #Pagination by 5
    paginator = Paginator(pos_list, 5)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    args = {'paginator': paginator,'filter':posfilter,
         'users':users,  'page':page, 'search':'netid',
         }
    # return render(request, 'search.html', {'filter': posfilter})
    return render(request, 'usersearch.html', args)

class UserUpdateView(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    permission_required = 'shared.User_Admin_Create'
    model = User
    form_class = UserForm
    template_name_suffix = '_user_form'

    def form_valid(self, form):
        #Existing Groups
        Advisor = Group.objects.get(name="Advisor_group")
        DGS = Group.objects.get(name="DGS_group")
        Admin = Group.objects.get(name="Administrators")
        Meng = Group.objects.get(name="MEng_students")
        MS = Group.objects.get(name="MS_students")
        PhD = Group.objects.get(name="PHD_students")

        #Get list of types for user
        types = form.instance.user_type

        # logger.error("My user is:")
        # logger.error(form.instance)
        # logger.error("My groups are:")
        # logger.error(form.instance.groups.all())

        #Clear all groups from User for Update View
        form.instance.groups.clear()

        #Booleans to check for student and professor privileges
        Meng_bool = False
        MS_bool = False
        PhD_bool = False
        Advisor_bool = False
        Admin_bool = False
        DGS_bool = False
        student = False
        professor = False

        #Checks to set booleans to later add user to groups
        if ('1' in types):
            Meng_bool = True
            student = True
            logger.error("Meng is TRUE")
        if ('2' in types):
            MS_bool = True
            student = True
            logger.error("MS is TRUE")
        if ('3' in types):
            PhD_bool = True
            student = True
            logger.error("PhD is TRUE")
        if ('4' in types):
            Advisor_bool = True
            professor = True
            logger.error("Advisor is TRUE")
        if ('5' in types):
            DGS_bool = True
            professor = True
            logger.error("DGS is TRUE")
        if ('6' in types):
            Admin_bool = True
            professor = True
            logger.error("Admin is TRUE")

        #Checks that user does not have student and professor privileges
        if ((student == True)&(professor == True)):
            messages.add_message(self.request, messages.ERROR, "Accounts may not have student privileges along with " \
            "DGS, Advisor, or Administrator privileges.")
            return redirect('admin-user-update', pk=self.kwargs.get("pk"))

        #Add user to correct groups
        if Meng_bool:
            Meng.user_set.add(form.instance)
        if MS_bool:
            MS.user_set.add(form.instance)
        if PhD_bool:
            PhD.user_set.add(form.instance)
        if Advisor_bool:
            Advisor.user_set.add(form.instance)
        if DGS_bool:
            DGS.user_set.add(form.instance)
        if Admin_bool:
            Admin.user_set.add(form.instance)

        logger.error("User groups are:")
        logger.error(form.instance.groups.all())

        return super(UserUpdateView, self).form_valid(form)


#Admin Function to Delete 1 Course
@permission_required('shared.User_Admin_Create')
def userdelete(request, form_id):
    form = get_object_or_404(User, pk=form_id)
    form.delete()
    return redirect('admin-user-search')


@permission_required('shared.User_Admin_Create')
def upload(request):
    if request.method == "GET":
        data = {}
        return render(request, "upload.html", data)
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return redirect('admin-student-upload')

        if csv_file.multiple_chunks():
            messages.error(request, 'Too large of a file')
            return redirect('admin-student-upload')

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")

        #Django Import Export Dataset
        headers = ('id', 'netid', 'email', 'first_name',
        'last_name', 'student_id', 'user_type', 'advisor', 'groups')
        dataset = tablib.Dataset([], headers=headers)

        #Testing dataset
        # single = tablib.Dataset([], headers=headers)
        # single.append(('', 'fl1', 'fakenew@gmail.com', 'Fake', 'Account', '25', "MEng", 'adh25'))
        for line in lines:
            fields = line.split(",")
            #Assign variables to each field in the line
            student_ID = fields[0]
            last_name = fields[1]
            first_name = fields[2]
            email = fields[3]
            netid = fields[4]
            student_type = fields[5]
            advisor = fields[6]
            MEng = 1
            MS = 2
            PhD = 3
            usertype = "None"
            mytype = 0
            # logger.error("ID is: "+str(student_ID))
            #Omit top row
            if (str(email) == "Email"):
                # logger.error("TOP ROW\n\n\n")
                continue
            logger.error("Last name is: "+str(last_name))
            logger.error("First name is: "+str(first_name))
            logger.error("Email is: "+str(email))
            logger.error("Netid is: "+str(netid))
            logger.error("Student type is: "+str(student_type))
            group = ''
            #Assign correct user types
            if student_type == "E-EGR-ECE":
                usertype = "MEng"
                mytype = 1
                group = 'MEng_students'
                # logger.error("MEng Student")
            elif student_type == "G-ECE-MS":
                usertype = "MS"
                mytype = 2
                group = 'MS_students'
                # logger.error("MS Student")
            elif student_type == "G-ECE-PHD":
                usertype = "PhD"
                mytype = 3
                group ='PHD_students'
                # logger.error("PhD Student")
            logger.error("Advisor is: "+str(advisor))
            advisor_real = advisor.rstrip()
            dataset.append(('', netid, email, first_name, last_name, student_ID, usertype, advisor_real, group))

        #Lose first row
        del dataset[0]

        # del single[0]

        logger.error("My dataset is:")
        logger.error(dataset.export('df'))

        # logger.error(single.export('df'))

        #user resource to import data
        user_resource = UserResource()

        #Dry run import
        result = user_resource.import_data(dataset, raise_errors=False, dry_run=True)
        if result.has_errors():
            errors = result.row_errors()
            messages.add_message(request, messages.ERROR, "DRY RUN IMPORT FAILED")
            logger.error("DRY RUN IMPORT FAILED!")
            return redirect('admin-student-upload')

        else:
            messages.add_message(request, messages.SUCCESS, "DRY RUN IMPORT SUCCESS!")
            logger.error("DRY RUN IMPORT SUCCESS!")

        # True import
        real_import = user_resource.import_data(dataset, dry_run=False)
        if real_import.has_errors():
            messages.add_message(request, messages.ERROR, "TRUE IMPORT FAILED")
            error_class = real_import.get_error_result_class()
            logger.error("TRUE IMPORT FAILED!")
            return redirect('admin-student-upload')
        else:
            messages.add_message(request, messages.SUCCESS, "TRUE IMPORT SUCCESS!")
            logger.error("TRUE IMPORT SUCCESS!")


    except Exception as e:
        logger.error("Unable to upload file. "+repr(e))
        messages.error(request, "Unable to upload file. "+repr(e))

    return redirect('admin-student-upload')


def duke_login(request):
    authorize = "https://oauth.oit.duke.edu/oauth/authorize.php"
    # resource = "https://oauth.oit.duke.edu/oauth/resource.php
    # authorize = "https://oauth.oit.duke.edu/authorize"
    client_id = config("CLIENT_ID")
    client_secret = config("CLIENT_SECRET")
    redirect_uri ="http%3A%2F%2Fvcm-4469.vm.duke.edu%3A8000%2FPOS%2Fexternal_login"
    scope = "basic"
    state = "1123"

    redirect_URL = authorize+"?"+"response_type=token" \
    +"&redirect_uri="+redirect_uri \
    +"&client_secret="+client_secret \
    +"&client_id="+client_id \
    +"&state="+state+"&scope=identity%3Anetid%3Aread"

    logger.error("Redirect is:"+redirect_URL)
    return redirect(redirect_URL)

#Function to Export Approved Users
def MEng_export_approved(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="MEngapprovedusers.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('MEng_Approved_Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Netid', 'First name', 'Last name', 'Email address', 'Student ID' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = User.objects.filter(Q(user_type__icontains="MEng")&Q()).values_list('netid', 'first_name', 'last_name', 'email', 'student_id')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
