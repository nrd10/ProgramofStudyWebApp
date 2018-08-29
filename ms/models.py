from django.db import models
from django.contrib.auth.models import User
from shared.models import Course, Concentration
from django.urls import reverse
import datetime
from django.conf import settings


#Time and Year Global Variables
FALL = "FALL "
SPRING = "SPRING "
SUMMER = "SUMMER "
TERMS = []
RESEARCHTERMS = []
for r in range(2018, (datetime.datetime.now().year+4)):
    fall = FALL + str(r)
    spring = SPRING + str(r)
    summer = SUMMER + str(r)
    TERMS.append((fall, fall))
    TERMS.append((spring, spring))
    RESEARCHTERMS.append((fall, fall))
    RESEARCHTERMS.append((spring, spring))
    RESEARCHTERMS.append((summer, summer))

#Grade Global Variables
GRADES = []
GRADES.append(("A+", "A+"))
GRADES.append(("A", "A"))
GRADES.append(("A-", "A-"))
GRADES.append(("B+", "B+"))
GRADES.append(("B", "B"))
GRADES.append(("B-", "B-"))
GRADES.append(("C+", "C+"))
GRADES.append(("C", "C"))
GRADES.append(("C-", "C-"))


#Form States
FORMSTATES = []
FORMSTATES.append(("New", "New"))
FORMSTATES.append(("AdvisorRejected", "AdvisorRejected"))
FORMSTATES.append(("DGSRejected", "DGSRejected"))
FORMSTATES.append(("AdvisorPending", "AdvisorPending"))
FORMSTATES.append(("DGSPending", "DGSPending"))
FORMSTATES.append(("Approved", "Approved"))

#Comment Author contenttypes
COMMENTS = []
COMMENTS.append(("Advisor", "Advisor"))
COMMENTS.append(("DGS", "DGS"))

# Create your models here.
class MSCoursePOS(models.Model):
    gradececourseone = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MScECEone",
    verbose_name = "Graduate ECE Course I")
    gradeceoneterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradeceonegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradececoursetwo = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="MScECEtwo",
    verbose_name = "Graduate ECE Course II")
    gradecetwoterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradecetwograde = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradececoursethree = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MScECEthree",
    verbose_name = "Graduate ECE Course III")
    gradecethreeterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradecethreegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradececoursefour = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MScECEfour",
    verbose_name = "Graduate ECE Course IV")
    gradecefourterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradecefourgrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradtechcourseone = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MScgradtechOne",
    verbose_name ="Graduate Technical Elective from ECE or other approved area Course I")
    gradtechoneterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradtechonegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradtechcoursetwo = models.ForeignKey(Course,  on_delete=models.SET_NULL, null = True, related_name="MScgradtechTwo",
    verbose_name = "Graduate Technical Elective from ECE or other approved area Course II")
    gradtechtwoterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradtechtwograde = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electiveone = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MScelectiveOne",
    verbose_name = "Elective I")
    electiveoneterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electiveonegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electivetwo = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MScelectiveTwo",
    verbose_name = "Elective II")
    electivetwoterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electivetwograde = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electivethree = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MScelectiveThree",
    verbose_name = "Elective III")
    electivethreeterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electivethreegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electivefour = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MScelectiveFour",
    verbose_name = "Elective IV")
    electivefourterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electivefourgrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    submission = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(max_length=20, choices=FORMSTATES, blank=True, default=FORMSTATES[0], help_text='POS Form State')


    class Meta:
        verbose_name = 'Coursework MS Form'
        verbose_name_plural = 'Coursework MS Forms'
        permissions = (("MSc_Student_View", "Student View MS Coursework Forms"),
        ("MSc_Student_Create", "Student Create MS Coursework Forms"),
        ("MSc_Advisor_View", "Advisor View MS Coursework Forms"),
        ("MSc_DGS_View", "DGS View MS Coursework Forms"),
        ("MSc_Admin_View", "Admin View MS Coursework Forms"),
        ("MSc_Admin_Create", "Admin Create MS Coursework Forms"),
        )


    def __str__(self):
        '''
        String to represent this object
        '''
        return '{0}'.format(self.id)

    def get_absolute_url(self):
        '''
        Returns the url to access a particular instance of the model.
        '''
        return reverse('mscourse-detail', args=[str(self.id)])

    def get_advisor_url(self):
        '''
        Returns the url to access a particular instance of the model for
        an advisor to view.
        '''
        return reverse('advisor-mscourse-detail', args=[str(self.id)])

    def get_dgs_url(self):
        '''
        Returns the url to access a particular instance of the model for
        DGS view.
        '''
        return reverse('dgs-mscourse-detail', args=[str(self.id)])

    def get_admin_url(self):
        '''
        Returns the url to access a particular instance of the model for
        Admin view.
        '''
        return reverse('admin-mscourse-detail', args=[str(self.id)])

    def getname(self):
        '''
        Return the object type.
        '''
        class_name = "MSCoursePOS"
        return class_name

class MSCourseComment(models.Model):
    form = models.ForeignKey(MSCoursePOS, on_delete=models.CASCADE, null = True, related_name='comments')
    created_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=2000, help_text="Please enter a comment explaining why this form is being rejected.")
    authortype = models.CharField(max_length=30, choices=COMMENTS, blank=True, help_text='Either DGS or Advisor Commenting')
    class Meta:
         verbose_name = 'Course Comment'
         verbose_name_plural = 'Course Comments'


class MSProjectPOS(models.Model):
    gradececourseone = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MSpECEone",
    verbose_name = "Graduate ECE Course I")
    gradeceoneterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradeceonegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradececoursetwo = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="MSpECEtwo",
    verbose_name = "Graduate ECE Course II")
    gradecetwoterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradecetwograde = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradececoursethree = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MSpECEthree",
    verbose_name = "Graduate ECE Course III")
    gradecethreeterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradecethreegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradececoursefour = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="MSpECEfour",
    verbose_name = "Graduate ECE Course IV")
    gradecefourterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradecefourgrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electiveone = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="MSpelectiveOne",
    verbose_name = "Elective I")
    electiveoneterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electiveonegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electivetwo = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="MSpelectiveTwo",
    verbose_name = "Elective II")
    electivetwoterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electivetwograde = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electivethree = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="MSpelectiveThree",
    verbose_name = "Elective III")
    electivethreeterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electivethreegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electivefour = models.ForeignKey(Course,  on_delete=models.SET_NULL, null = True,  related_name="MSpelectiveFour",
    verbose_name = "Elective IV")
    electivefourterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electivefourgrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electivefive = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MSpelectiveFive",
    verbose_name = "Elective V")
    electivefiveterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electivefivegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    researchcourseterm = models.CharField(max_length=20,choices=RESEARCHTERMS, default=RESEARCHTERMS[0],
    verbose_name = "Research Credit I Term")
    researchcoursegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    submission = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(max_length=20, choices=FORMSTATES, blank=True, default=FORMSTATES[0], help_text='POS Form State')

    class Meta:
        verbose_name = 'Project MS Form'
        verbose_name_plural = 'Project MS Forms'
        permissions = (("MSp_Student_View", "Student View MS Project Forms"),
        ("MSp_Student_Create", "Student Create MS Project Forms"),
        ("MSp_Advisor_View", "Advisor View MS Project Forms"),
        ("MSp_DGS_View", "DGS View MS Project Forms"),
        ("MSp_Admin_View", "Admin View MS Project Forms"),
        ("MSp_Admin_Create", "Admin Create MS Project Forms"),
        )


    def __str__(self):
        '''
        String to represent this object
        '''
        return '{0}'.format(self.id)

    def get_absolute_url(self):
        '''
        Returns the url to access a particular instance of the model.
        '''
        return reverse('msproject-detail', args=[str(self.id)])

    def get_advisor_url(self):
        '''
        Returns the url to access a particular instance of the model for
        an advisor to view.
        '''
        return reverse('advisor-msproject-detail', args=[str(self.id)])

    def get_dgs_url(self):
        '''
        Returns the url to access a particular instance of the model for
        DGS view.
        '''
        return reverse('dgs-msproject-detail', args=[str(self.id)])

    def get_admin_url(self):
        '''
        Returns the url to access a particular instance of the model for
        Admin view.
        '''
        return reverse('admin-msproject-detail', args=[str(self.id)])

    def getname(self):
        '''
        Return the object type.
        '''
        class_name = "MSProjectPOS"
        return class_name

class MSProjectComment(models.Model):
    form = models.ForeignKey(MSProjectPOS, on_delete=models.CASCADE, null = True, related_name='comments')
    created_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=2000, help_text="Please enter a comment explaining why this form is being rejected.")
    authortype = models.CharField(max_length=30, choices=COMMENTS, blank=True, help_text='Either DGS or Advisor Commenting')
    class Meta:
         verbose_name = 'Project Comment'
         verbose_name_plural = 'Project Comments'


class MSThesisPOS(models.Model):
    gradececourseone = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MStECEone",
    verbose_name = "Graduate ECE Course I")
    gradeceoneterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradeceonegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradececoursetwo = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="MStECEtwo",
    verbose_name = "Graduate ECE Course II")
    gradecetwoterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradecetwograde = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradececoursethree = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MStECEthree",
    verbose_name = "Graduate ECE Course III")
    gradecethreeterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradecethreegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradececoursefour = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="MStECEfour",
    verbose_name = "Graduate ECE Course IV")
    gradecefourterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradecefourgrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electiveone = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="MStelectiveOne",
    verbose_name = "Elective I")
    electiveoneterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electiveonegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electivetwo = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="MStelectiveTwo",
    verbose_name = "Elective II")
    electivetwoterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electivetwograde = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electivethree = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="MStelectiveThree",
    verbose_name = "Elective III")
    electivethreeterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electivethreegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electivefour = models.ForeignKey(Course,  on_delete=models.SET_NULL, null = True,  related_name="MStelectiveFour",
    verbose_name = "Elective IV")
    electivefourterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electivefourgrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    researchcourseterm = models.CharField(max_length=20,choices=RESEARCHTERMS, verbose_name =
     "Research Credit Semester I", default=RESEARCHTERMS[0])
    researchcoursegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)
    researchcoursetermtwo = models.CharField(max_length=20,choices=RESEARCHTERMS,
    verbose_name = "Research Credit Semester II", default=RESEARCHTERMS[0])
    researchcoursetwograde = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    submission = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(max_length=20, choices=FORMSTATES, blank=True, default=FORMSTATES[0], help_text='POS Form State')

    class Meta:
        verbose_name = 'Thesis MS Form'
        verbose_name_plural = 'Thesis MS Forms'
        permissions = (("MSt_Student_View", "Student View MS Thesis Forms"),
        ("MSt_Student_Create", "Student Create MS Thesis Forms"),
        ("MSt_Advisor_View", "Advisor View MS Thesis Forms"),
        ("MSt_DGS_View", "DGS View MS Thesis Forms"),
        ("MSt_Admin_View", "Admin View MS Thesis Forms"),
        ("MSt_Admin_Create", "Admin Create MS Thesis Forms"),
        )

    def __str__(self):
        '''
        String to represent this object
        '''
        return '{0}'.format(self.id)

    def get_absolute_url(self):
        '''
        Returns the url to access a particular instance of the model.
        '''
        return reverse('msthesis-detail', args=[str(self.id)])

    def get_advisor_url(self):
        '''
        Returns the url to access a particular instance of the model for
        an advisor to view.
        '''
        return reverse('advisor-msthesis-detail', args=[str(self.id)])

    def get_dgs_url(self):
        '''
        Returns the url to access a particular instance of the model for
        DGS view.
        '''
        return reverse('dgs-msthesis-detail', args=[str(self.id)])

    def get_admin_url(self):
        '''
        Returns the url to access a particular instance of the model for
        Admin view.
        '''
        return reverse('admin-msthesis-detail', args=[str(self.id)])

    def getname(self):
        '''
        Return the object type.
        '''
        class_name = "MSThesisPOS"
        return class_name

class MSThesisComment(models.Model):
    form = models.ForeignKey(MSThesisPOS, on_delete=models.CASCADE, null = True, related_name='comments')
    created_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=2000, help_text="Please enter a comment explaining why this form is being rejected.")
    authortype = models.CharField(max_length=30, choices=COMMENTS, blank=True, help_text='Either DGS or Advisor Commenting')
    class Meta:
         verbose_name = 'Thesis Comment'
         verbose_name_plural = 'Thesis Comments'
