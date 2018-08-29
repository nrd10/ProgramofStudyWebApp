from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField
from django.db.models import Q #allows for complex queries
from django.utils.html import escape
from phd.models import *
from shared.models import *
from django_select2.forms import Select2Widget
from shared.models import Course, Concentration

import logging

logger = logging.getLogger('phd/forms.py')


class PHDBSPOSForm(ModelForm):
    class Meta:
        model = PHDBachelorPOS
        exclude = ('owner', 'state')

    #Django Select2 Fields
    secondaryadvisor = ModelChoiceField(label="Additional Faculty", queryset=User.objects.filter(Q(user_type__icontains="Advisor")), widget=Select2Widget)
    curriculararea = ModelChoiceField(label="ECE Curricular Area", queryset=CurricularArea.objects.all(), widget=Select2Widget)
    gradececourseone = ModelChoiceField(label="Graduate ECE Course I", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursetwo = ModelChoiceField(label="Graduate ECE Course II", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursethree = ModelChoiceField(label="Graduate ECE Course III", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursefour = ModelChoiceField(label="Graduate ECE Course IV", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursefive = ModelChoiceField(label="Graduate ECE Course V", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursesix = ModelChoiceField(label="Graduate ECE Course VI", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    electiveone = ModelChoiceField(label="Elective I", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivetwo = ModelChoiceField(label="Elective II", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    gradtechcourseone = ModelChoiceField(label="Graduate Technical Elective from ECE or other approved area Course I", queryset=Course.objects.filter(Q(category__title__iexact="Approved Technical Elective")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradtechcoursetwo = ModelChoiceField(label="Graduate Technical Elective from ECE or other approved area Course II", queryset=Course.objects.filter(Q(category__title__iexact="Approved Technical Elective")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)


    def clean(self):
        cleaned_data = super().clean()
        eceone = cleaned_data.get("gradececourseone")
        ecetwo = cleaned_data.get("gradececoursetwo")
        ecethree = cleaned_data.get("gradececoursethree")
        ecefour = cleaned_data.get("gradececoursefour")
        ecefive = cleaned_data.get("gradececoursefive")
        ecesix = cleaned_data.get("gradececoursesix")
        electiveone = cleaned_data.get("electiveone")
        electivetwo = cleaned_data.get("electivetwo")
        gradtechcourseone = cleaned_data.get("gradtechcourseone")
        gradtechcoursetwo = cleaned_data.get("gradtechcoursetwo")
        #counter for ECE 899: Independent Study
        indcount = 0
        #counter for Undergrad Courses
        undergrad = 0
        empty = False

        if ((electiveone is None) or (electivetwo is None)):
            empty = True

        #Indepdent Study Count Check
        if (empty is False):
            if (electiveone.listing == "ECE 899"):
                indcount = indcount + 1

            if (electivetwo.listing == "ECE 899"):
                indcount = indcount + 1

        #Undergraduate Course Count Check
        if (empty is False):
            if (("ECE 3" in electiveone.listing) or ("ECE 4" in electiveone.listing)):
                undergrad = undergrad +1

            if (("ECE 3" in electivetwo.listing) or ("ECE 4" in electivetwo.listing)):
                undergrad = undergrad + 1

        logger.error("ind count is:"+str(indcount))
        logger.error("undergrad count is:"+str(undergrad))
        logger.error("total is:"+str(undergrad+indcount))

        #Statments below check whether too many undergraduate courses along with independent studies
        if (undergrad + indcount > 2):
            self._errors['electiveone'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']
            self._errors['electivetwo'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']

        #Below checks if any fields are duplicates
        if ((eceone==ecetwo) or (eceone==ecethree) or (eceone==ecefour)
        or (eceone==ecefive) or (eceone==ecesix) or (eceone==gradtechcourseone)
        or (eceone==gradtechcoursetwo) or (eceone==electiveone) or (eceone==electivetwo)):
            self._errors['gradececourseone'] = [u'Graduate ECE Course I cannot be the same as any other course.']

        if ((ecetwo==ecethree) or (ecetwo==ecefour) or (ecetwo==ecefive)
        or (ecetwo==ecesix) or (ecetwo==gradtechcourseone)
        or (ecetwo==gradtechcoursetwo) or (ecetwo==electiveone) or (ecetwo==electivetwo)):
            self._errors['gradececoursetwo'] = [u'Graduate ECE Course II cannot be the same as any other course.']

        if ((ecethree==ecefour) or (ecethree==ecefive) or (ecethree==ecesix)
        or (ecethree==gradtechcourseone) or (ecethree==gradtechcoursetwo)
        or (ecethree==electiveone) or (ecethree==electivetwo)):
            self._errors['gradececoursethree'] = [u'Graduate ECE Course III cannot be the same as any other course.']

        if ((ecefour==ecefive) or (ecefour==ecesix)
        or (ecefour==gradtechcourseone) or (ecefour==gradtechcoursetwo)
        or (ecefour==electiveone) or (ecefour==electivetwo)):
            self._errors['gradececoursefour'] = [u'Graduate ECE Course IV cannot be the same as any other course.']

        if ((ecefive==ecesix) or (ecefive==gradtechcourseone)
        or (ecefive==gradtechcoursetwo) or (ecefive==electiveone)
        or (ecefive==electivetwo)):
            self._errors['gradececoursefive'] = [u'Graduate ECE Course V cannot be the same as any other course.']

        if ((ecesix==gradtechcourseone) or (ecesix==gradtechcoursetwo)
        or (ecesix==electiveone) or (ecesix==electivetwo)):
            self._errors['gradececoursesix'] = [u'Graduate ECE Course VI cannot be the same as any other course.']

        if ((gradtechcourseone==gradtechcoursetwo) or (gradtechcourseone==electiveone)
        or (gradtechcourseone==electivetwo)):
            self._errors['gradtechcourseone'] = [u'Graduate Technical Elective I cannot be the same as any other course.']

        if ((gradtechcoursetwo==electiveone) or (gradtechcoursetwo==electivetwo)):
            self._errors['gradtechcoursetwo'] = [u'Graduate Technical Elective II cannot be the same as any other course.']

        if ((electiveone==electivetwo)):
            if (empty is False):
                if (electiveone.listing != "ECE 899"):    #
                    self._errors['electiveone'] = [u'Elective I cannot be the same as any other course.']

class PHDBachelorCommentForm(ModelForm):
    class Meta:
        model = PHDBachelorComment
        exclude = ('created_date', 'authortype', 'form')


class AdminPHDBSPOSForm(ModelForm):
    class Meta:
        model = PHDBachelorPOS
        exclude = ( 'state',)

    #Django Select2 Fields

    owner = ModelChoiceField(label="Owner", queryset=User.objects.filter(Q(user_type__icontains="PhD")), widget=Select2Widget)
    secondaryadvisor = ModelChoiceField(label="Additional Faculty", queryset=User.objects.filter(Q(user_type__icontains="Advisor")), widget=Select2Widget)
    curriculararea = ModelChoiceField(label="ECE Curricular Area", queryset=CurricularArea.objects.all(), widget=Select2Widget)
    gradececourseone = ModelChoiceField(label="Graduate ECE Course I", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursetwo = ModelChoiceField(label="Graduate ECE Course II", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursethree = ModelChoiceField(label="Graduate ECE Course III", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursefour = ModelChoiceField(label="Graduate ECE Course IV", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursefive = ModelChoiceField(label="Graduate ECE Course V", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursesix = ModelChoiceField(label="Graduate ECE Course VI", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    electiveone = ModelChoiceField(label="Elective I", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivetwo = ModelChoiceField(label="Elective II", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    gradtechcourseone = ModelChoiceField(label="Graduate Technical Elective from ECE or other approved area Course I", queryset=Course.objects.filter(Q(category__title__iexact="Approved Technical Elective")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradtechcoursetwo = ModelChoiceField(label="Graduate Technical Elective from ECE or other approved area Course II", queryset=Course.objects.filter(Q(category__title__iexact="Approved Technical Elective")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)



class PHDMSPOSForm(ModelForm):
    class Meta:
        model = PHDMasterPOS
        exclude = ('owner', 'state')

    #Django Select2 Fields
    secondaryadvisor = ModelChoiceField(label="Additional Faculty", queryset=User.objects.filter(Q(user_type__icontains="PhD")), widget=Select2Widget)
    curriculararea = ModelChoiceField(label="ECE Curricular Area", queryset=CurricularArea.objects.all(), widget=Select2Widget)
    gradececourseone = ModelChoiceField(label="Graduate ECE Course I", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursetwo = ModelChoiceField(label="Graduate ECE Course II", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursethree = ModelChoiceField(label="Graduate ECE Course III", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    electiveone = ModelChoiceField(label="Elective I", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    gradtechcourseone = ModelChoiceField(label="Graduate Technical Elective from ECE or other approved area Course I", queryset=Course.objects.filter(Q(category__title__iexact="Approved Technical Elective")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)


    def clean(self):
        cleaned_data = super().clean()
        eceone = cleaned_data.get("gradececourseone")
        ecetwo = cleaned_data.get("gradececoursetwo")
        ecethree = cleaned_data.get("gradececoursethree")
        electiveone = cleaned_data.get("electiveone")
        gradtechcourseone = cleaned_data.get("gradtechcourseone")
        #counter for ECE 899: Independent Study
        indcount = 0
        #counter for Undergrad Courses
        undergrad = 0
        empty = False

        if (electiveone is None):
            empty = True

        #Indepdent Study Count Check
        if (empty is False):
            if (electiveone.listing == "ECE 899"):
                indcount = indcount + 1

        #Undergraduate Course Count Check
        if (empty is False):
            if (("ECE 3" in electiveone.listing) or ("ECE 4" in electiveone.listing)):
                undergrad = undergrad +1

        logger.error("ind count is:"+str(indcount))
        logger.error("undergrad count is:"+str(undergrad))
        logger.error("total is:"+str(undergrad+indcount))

        #Statments below check whether too many undergraduate courses along with independent studies
        if (undergrad + indcount > 2):
            self._errors['electiveone'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']

        #Below checks if any fields are duplicates
        if ((eceone==ecetwo) or (eceone==ecethree)
        or (eceone==gradtechcourseone)
        or (eceone==electiveone)):
            self._errors['gradececourseone'] = [u'Graduate ECE Course I cannot be the same as any other course.']

        if ((ecetwo==ecethree) or (ecetwo==gradtechcourseone)
        or (ecetwo==electiveone)):
            self._errors['gradececoursetwo'] = [u'Graduate ECE Course II cannot be the same as any other course.']

        if ((ecethree==gradtechcourseone) or (ecethree==electiveone)):
            self._errors['gradececoursethree'] = [u'Graduate ECE Course III cannot be the same as any other course.']

        if (gradtechcourseone==electiveone):
            self._errors['gradtechcourseone'] = [u'Graduate Technical Elective I cannot be the same as any other course.']


class PHDMasterCommentForm(ModelForm):
    class Meta:
        model = PHDMasterComment
        exclude = ('created_date', 'authortype', 'form')


class AdminPHDMSPOSForm(ModelForm):
    class Meta:
        model = PHDMasterPOS
        exclude = ( 'state',)

    #Django Select2 Fields
    owner = ModelChoiceField(label="Owner", queryset=User.objects.filter(Q(user_type__icontains="PhD")), widget=Select2Widget)
    secondaryadvisor = ModelChoiceField(label="Additional Faculty", queryset=User.objects.filter(Q(user_type__icontains="Advisor")), widget=Select2Widget)
    curriculararea = ModelChoiceField(label="ECE Curricular Area", queryset=CurricularArea.objects.all(), widget=Select2Widget)
    gradececourseone = ModelChoiceField(label="Graduate ECE Course I", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursetwo = ModelChoiceField(label="Graduate ECE Course II", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursethree = ModelChoiceField(label="Graduate ECE Course III", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    electiveone = ModelChoiceField(label="Elective I", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    gradtechcourseone = ModelChoiceField(label="Graduate Technical Elective from ECE or other approved area Course I", queryset=Course.objects.filter(Q(category__title__iexact="Approved Technical Elective")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
