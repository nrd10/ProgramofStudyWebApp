from django.db import models
from django.contrib.auth.models import User
from shared.models import Course, Concentration
from django.urls import reverse
from django.conf import settings
import datetime


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

class MEngPOS(models.Model):
    '''
    Model for storing Program of Study forms for MEng students
    '''
    coreclassone = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, blank=True,
    related_name = "Mengcoreone", verbose_name = "Core Industry Prep Course I")
    coreterm = models.CharField(max_length=20,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    coreonegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    coreclasstwo = models.ForeignKey(Course,  on_delete=models.SET_NULL, null = True, blank=True,
    related_name = "Mengcoretwo", verbose_name = "Core Industry Prep Course II")
    coretwoterm = models.CharField(max_length=20,choices=TERMS, verbose_name =
    "Term",  default=TERMS[0])
    coretwograde = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    concentration = models.ForeignKey(Concentration, on_delete=models.SET_NULL, null=True)
    techcourseone = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MEngtechONE",
    verbose_name = "Concentration Area Course I")
    techoneterm = models.CharField(max_length=20,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    techonegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    techcoursetwo = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MEngtechTWO",
    verbose_name = "Concentration Area Course II ")
    techtwoterm = models.CharField(max_length=20,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    techtwograde = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    techcoursethree = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MEngtechThree",
    verbose_name = "Concentration Course III")
    techthreeterm = models.CharField(max_length=20,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    techthreegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradtechcourseone = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MEnggradtechOne",
    verbose_name ="Graduate Technical Elective from ECE or other approved area Course I")
    gradtechoneterm = models.CharField(max_length=20,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradtechonegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradtechcoursetwo = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MEnggradtechTwo",
    verbose_name = "Graduate Technical Elective from ECE or other approved area Course II")
    gradtechtwoterm = models.CharField(max_length=20,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradtechtwograde = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electiveone = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MEngelectiveOne",
    verbose_name = "Elective I")
    electiveoneterm = models.CharField(max_length=20,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electiveonegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electivetwo = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MEngelectiveTwo",
    verbose_name = "Elective II")
    electivetwoterm = models.CharField(max_length=20,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electivetwograde = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electivethree = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="MEngelectiveThree",
    verbose_name = "Elective III")
    electivethreeterm = models.CharField(max_length=20,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electivethreegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    submission = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    # POS_STATE = (
    #         ('1', 'New'),
    #         ('2', 'Rejected'),
    #         ('3', 'AdvisorPending'),
    #         ('4', 'DGSPending'),
    #         ('5', 'Approved'),
    #     )
    state = models.CharField(max_length=20, choices=FORMSTATES, blank=True, default=FORMSTATES[0], help_text='POS Form State')

    class Meta:
        verbose_name = 'MEng Form'
        verbose_name_plural = 'MEng Forms'
        permissions = (("MEng_Student_View", "Student View MEng Forms"),
        ("MEng_Student_Create", "Student Create MEng Forms"),
        ("MEng_Advisor_View", "Advisor View MEng Forms"),
        ("MEng_DGS_View", "DGS View MEng Forms"),
        ("MEng_Admin_View", "Admin View MEng Forms"),
        ("MEng_Admin_Create", "Admin Create MEng Forms"),
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
        return reverse('meng-detail', args=[str(self.id)])

    def get_advisor_url(self):
        '''
        Returns the url to access a particular instance of the model for
        an advisor to view.
        '''
        return reverse('advisor-meng-detail', args=[str(self.id)])

    def get_dgs_url(self):
        '''
        Returns the url to access a particular instance of the model for
        DGS view.
        '''
        return reverse('dgs-meng-detail', args=[str(self.id)])

    def get_admin_url(self):
        '''
        Returns the url to access a particular instance of the model for
        Admin view.
        '''
        return reverse('admin-meng-detail', args=[str(self.id)])


    def getname(self):
        '''
        Return the object type.
        '''
        class_name = "MEngPOS"
        return class_name

class MEngComment(models.Model):
    form = models.ForeignKey(MEngPOS, on_delete=models.CASCADE, null = True, related_name='comments')
    created_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=2000, help_text="Please enter a comment explaining why this form is being rejected.")
    authortype = models.CharField(max_length=30, choices=COMMENTS, blank=True, help_text='Either DGS or Advisor Commenting')
    class Meta:
         verbose_name = 'MEng Comment'
         verbose_name_plural = 'MEng Comment'
