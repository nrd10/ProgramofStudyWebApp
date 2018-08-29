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
class CurricularArea(models.Model):
    '''
    Model for representing each Concentration Area
    '''
    title = models.CharField(max_length=100, help_text="Enter a Curricular Area for PhD (e.g. Computer Engineering, Engineering Physics, etc.)")

    def __str__(self):
        '''
        String to represent this object
        '''
        return self.title


class PHDBachelorPOS(models.Model):
    curriculararea = models.ForeignKey(CurricularArea, on_delete=models.SET_NULL, null = True,
    related_name="PHDBScurricular_area", verbose_name = "ECE Curricular Area")
    gradececourseone = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="PhDBSECEone",
    verbose_name = "Graduate ECE Course I")
    gradeceoneterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradeceonegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradececoursetwo = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="PhDBSECEtwo",
    verbose_name = "Graduate ECE Course II")
    gradecetwoterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradecetwograde = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradececoursethree = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="PhDBSECEthree",
    verbose_name = "Graduate ECE Course III")
    gradecethreeterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradecethreegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradececoursefour = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="PhDBSECEfour",
    verbose_name = "Graduate ECE Course IV")
    gradecefourterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradecefourgrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradececoursefive = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="PhDBSECEfive",
    verbose_name = "Graduate ECE Course V")
    gradecefiveterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradecefivegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradececoursesix = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="PhDBSECEsix",
    verbose_name = "Graduate ECE Course VI")
    gradecesixterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradecesixgrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradtechcourseone = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="PhDBSgradtechOne",
    verbose_name ="Graduate Technical Elective from ECE or other approved area Course I")
    gradtechoneterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradtechonegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradtechcoursetwo = models.ForeignKey(Course,  on_delete=models.SET_NULL, null = True, related_name="PhDBSgradtechTwo",
    verbose_name = "Graduate Technical Elective from ECE or other approved area Course II")
    gradtechtwoterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradtechtwograde = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electiveone = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="PhDBSelectiveOne",
    verbose_name = "Elective I")
    electiveoneterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electiveonegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electivetwo = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="PhDBSelectiveTwo",
    verbose_name = "Elective II")
    electivetwoterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electivetwograde = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)


    submission = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    secondaryadvisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="Second_Advisor_Bachelor")
    state = models.CharField(max_length=20, choices=FORMSTATES, blank=True, default=FORMSTATES[0], help_text='POS Form State')

    class Meta:
        verbose_name = 'PhD BS Form'
        verbose_name_plural = 'PhD BS Forms'
        permissions = (("PHDBS_Student_View", "Student View PhD BS Forms"),
        ("PHDBS_Student_Create", "Student Create PhD BS Forms"),
        ("PHDBS_Advisor_View", "Advisor View PhD BS Forms"),
        ("PHDBS_DGS_View", "DGS View PhD BS Forms"),
        ("PHDBS_Admin_View", "Admin View PhD BS Forms"),
        ("PHDBS_Admin_Create", "Admin Create PhD BS Forms"),
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
        return reverse('phdbachelor-detail', args=[str(self.id)])

    def get_advisor_url(self):
        '''
        Returns the url to access a particular instance of the model for
        an advisor to view.
        '''
        return reverse('advisor-phdbachelor-detail', args=[str(self.id)])

    def get_dgs_url(self):
        '''
        Returns the url to access a particular instance of the model for
        DGS view.
        '''
        return reverse('dgs-phdbachelor-detail', args=[str(self.id)])


class PHDBachelorComment(models.Model):
    form = models.ForeignKey(PHDBachelorPOS, on_delete=models.CASCADE, null = True, related_name='comments')
    created_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=2000, help_text="Please enter a comment explaining why this form is being rejected.")
    authortype = models.CharField(max_length=30, choices=COMMENTS, blank=True, help_text='Either DGS or Advisor Commenting')
    class Meta:
         verbose_name = 'PHD Bachelor Comment'
         verbose_name_plural = 'PHD Bachelor Comments'

class PHDMasterPOS(models.Model):
    curriculararea = models.ForeignKey(CurricularArea, on_delete=models.SET_NULL, null = True,
    related_name="PHDMScurricular_area", verbose_name = "ECE Curricular Area")
    gradececourseone = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="PhDMSECEone",
    verbose_name = "Graduate ECE Course I")
    gradeceoneterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradeceonegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradececoursetwo = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="PhDMSECEtwo",
    verbose_name = "Graduate ECE Course II")
    gradecetwoterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradecetwograde = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradececoursethree = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="PhDMSECEthree",
    verbose_name = "Graduate ECE Course III")
    gradecethreeterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradecethreegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    gradtechcourseone = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True, related_name="PhDMSgradtechOne",
    verbose_name ="Graduate Technical Elective from ECE or other approved area Course I")
    gradtechoneterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    gradtechonegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    electiveone = models.ForeignKey(Course, on_delete=models.SET_NULL, null = True,  related_name="PhDMSelectiveOne",
    verbose_name = "Elective I")
    electiveoneterm = models.CharField(max_length=30,choices=TERMS, verbose_name =
    "Term", default=TERMS[0])
    electiveonegrade = models.CharField(max_length=5,choices=GRADES, verbose_name =
    "Grade", blank=True)

    submission = models.DateTimeField(auto_now_add=True)
    secondaryadvisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="Second_Advisor_Master")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(max_length=20, choices=FORMSTATES, blank=True, default=FORMSTATES[0], help_text='POS Form State')

    class Meta:
        verbose_name = 'PhD MS Form'
        verbose_name_plural = 'PhD MS Forms'
        permissions = (("PHDMS_Student_View", "Student View PhD MS Forms"),
        ("PHDMS_Student_Create", "Student Create PhD MS Forms"),
        ("PHDMS_Advisor_View", "Advisor View PhD MS Forms"),
        ("PHDMS_DGS_View", "DGS View PhD MS Forms"),
        ("PHDMS_Admin_View", "Admin View PhD MS Forms"),
        ("PHDMS_Admin_Create", "Admin Create PhD MS Forms"),
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
        return reverse('phdmaster-detail', args=[str(self.id)])

    def get_advisor_url(self):
        '''
        Returns the url to access a particular instance of the model for
        an advisor to view.
        '''
        return reverse('advisor-phdmaster-detail', args=[str(self.id)])

    def get_dgs_url(self):
        '''
        Returns the url to access a particular instance of the model for
        DGS view.
        '''
        return reverse('dgs-phdmaster-detail', args=[str(self.id)])



class PHDMasterComment(models.Model):
    form = models.ForeignKey(PHDMasterPOS, on_delete=models.CASCADE, null = True, related_name='comments')
    created_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=2000, help_text="Please enter a comment explaining why this form is being rejected.")
    authortype = models.CharField(max_length=30, choices=COMMENTS, blank=True, help_text='Either DGS or Advisor Commenting')
    class Meta:
         verbose_name = 'PHD Master Comment'
         verbose_name_plural = 'PHD Master Comments'
