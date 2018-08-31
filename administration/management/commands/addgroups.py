from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from shared.models import User as CustomUser
from meng.models import *
from ms.models import *
from phd.models import *
import logging

logger = logging.getLogger('administration/management/addgroupss.py')

#This command will email all Advisors how many forms they need to edit
class Command(BaseCommand):

    def handle(self, *args, **options):
        #Get all DGS accounts

        MEng_students, mengbool = Group.objects.get_or_create(name = 'MEng_students')
        MS_students, MSbool = Group.objects.get_or_create(name = 'MS_students')
        Advisor_group, Advisebool = Group.objects.get_or_create(name = 'Advisor_group')
        DGS_group, DGSbool = Group.objects.get_or_create(name = 'DGS_group')
        PHD_students, phdbool = Group.objects.get_or_create(name = 'PHD_students')
        Administrators, adminbool = Group.objects.get_or_create(name = 'Administrators')

        self.stdout.write(self.style.SUCCESS('ALL GROUPS ADDED'))


        MEng_View = Permission.objects.get(codename="MEng_Student_View")
        MEng_Create = Permission.objects.get(codename="MEng_Student_Create")

        MEng_students.permissions.add(MEng_View)
        MEng_students.permissions.add(MEng_Create)

        self.stdout.write(self.style.SUCCESS('MEng STUDENT PERMISSIONS ADDED'))

        MSc_View = Permission.objects.get(codename="MSc_Student_View")
        MSc_Create = Permission.objects.get(codename="MSc_Student_Create")
        MSp_View = Permission.objects.get(codename="MSp_Student_View")
        MSp_Create = Permission.objects.get(codename="MSp_Student_Create")
        MSt_View = Permission.objects.get(codename="MSt_Student_View")
        MSt_Create = Permission.objects.get(codename="MSt_Student_Create")

        MS_students.permissions.add(MSc_View)
        MS_students.permissions.add(MSc_Create)
        MS_students.permissions.add(MSp_View)
        MS_students.permissions.add(MSp_Create)
        MS_students.permissions.add(MSt_View)
        MS_students.permissions.add(MSt_Create)

        self.stdout.write(self.style.SUCCESS('MS STUDENT PERMISSIONS ADDED'))

        PHDb_View = Permission.objects.get(codename="PHDBS_Student_View")
        PHDb_Create = Permission.objects.get(codename="PHDBS_Student_Create")
        PHDm_View = Permission.objects.get(codename="PHDMS_Student_View")
        PHDm_Create = Permission.objects.get(codename="PHDMS_Student_Create")

        PHD_students.permissions.add(MSc_View)
        PHD_students.permissions.add(MSc_Create)
        PHD_students.permissions.add(MSp_View)
        PHD_students.permissions.add(MSp_Create)

        self.stdout.write(self.style.SUCCESS('PHD STUDENT PERMISSIONS ADDED'))

        MEng_advise = Permission.objects.get(codename="MEng_Advisor_View")
        MSc_advise = Permission.objects.get(codename="MSc_Advisor_View")
        MSp_advise = Permission.objects.get(codename="MSp_Advisor_View")
        MSt_advise = Permission.objects.get(codename="MSt_Advisor_View")
        PhDb_advise = Permission.objects.get(codename="PHDBS_Advisor_View")
        PhDm_advise = Permission.objects.get(codename="PHDMS_Advisor_View")

        Advisor_group.permissions.add(MEng_advise)
        Advisor_group.permissions.add(MSc_advise)
        Advisor_group.permissions.add(MSp_advise)
        Advisor_group.permissions.add(MSt_advise)
        Advisor_group.permissions.add(PhDb_advise)
        Advisor_group.permissions.add(PhDm_advise)

        self.stdout.write(self.style.SUCCESS('Advisor PERMISSIONS ADDED'))

        MEng_DGS = Permission.objects.get(codename="MEng_DGS_View")
        MSc_DGS = Permission.objects.get(codename="MSc_DGS_View")
        MSp_DGS = Permission.objects.get(codename="MSp_DGS_View")
        MSt_DGS = Permission.objects.get(codename="MSt_DGS_View")
        PhDb_DGS = Permission.objects.get(codename="PHDBS_DGS_View")
        PhDm_DGS = Permission.objects.get(codename="PHDMS_DGS_View")

        DGS_group.permissions.add(MEng_DGS)
        DGS_group.permissions.add(MSc_DGS)
        DGS_group.permissions.add(MSp_DGS)
        DGS_group.permissions.add(MSt_DGS)
        DGS_group.permissions.add(PhDb_DGS)
        DGS_group.permissions.add(PhDm_DGS)

        self.stdout.write(self.style.SUCCESS('DGS PERMISSIONS ADDED'))

        MEng_Admin_View = Permission.objects.get(codename="MEng_Admin_View")
        MEng_Admin_Create = Permission.objects.get(codename="MEng_Admin_Create")
        MSc_Admin_View = Permission.objects.get(codename="MSc_Admin_View")
        MSc_Admin_Create = Permission.objects.get(codename="MSc_Admin_Create")
        MSp_Admin_View = Permission.objects.get(codename="MSp_Admin_View")
        MSp_Admin_Create = Permission.objects.get(codename="MSp_Admin_Create")
        MSt_Admin_View = Permission.objects.get(codename="MSt_Admin_View")
        MSt_Admin_Create = Permission.objects.get(codename="MSt_Admin_Create")
        PHDBS_Admin_View = Permission.objects.get(codename="PHDBS_Admin_View")
        PHDBS_Admin_Create = Permission.objects.get(codename="PHDBS_Admin_Create")
        PHDMS_Admin_View = Permission.objects.get(codename="PHDMS_Admin_View")
        PHDMS_Admin_Create = Permission.objects.get(codename="PHDMS_Admin_Create")
        Course_Admin_Create = Permission.objects.get(codename="Course_Admin_Create")
        User_Admin_Create = Permission.objects.get(codename="User_Admin_Create")

        Administrators.permissions.add(MEng_Admin_View)
        Administrators.permissions.add(MEng_Admin_Create)
        Administrators.permissions.add(MSc_Admin_View)
        Administrators.permissions.add(MSc_Admin_Create)
        Administrators.permissions.add(MSp_Admin_View)
        Administrators.permissions.add(MSp_Admin_Create)
        Administrators.permissions.add(MSt_Admin_View)
        Administrators.permissions.add(MSt_Admin_Create)
        Administrators.permissions.add(PHDBS_Admin_View)
        Administrators.permissions.add(PHDBS_Admin_Create)
        Administrators.permissions.add(PHDMS_Admin_View)
        Administrators.permissions.add(PHDMS_Admin_Create)
        Administrators.permissions.add(Course_Admin_Create)
        Administrators.permissions.add(User_Admin_Create)

        self.stdout.write(self.style.SUCCESS('Admin PERMISSIONS ADDED'))

        self.stdout.write(self.style.SUCCESS('ALL PERMISSIONS ADDED'))
