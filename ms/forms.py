from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField
from django.db.models import Q #allows for complex queries
from django.utils.html import escape
from ms.models import *
from shared.models import *
from django_select2.forms import Select2Widget
from shared.models import Course, Concentration

import logging

logger = logging.getLogger('ms/forms.py')


class MSCoursePOSForm(ModelForm):
    class Meta:
        model = MSCoursePOS
        exclude = ('owner', 'state')

    #Django Select2 Fields
    gradececourseone = ModelChoiceField(label="Graduate ECE Course I", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursetwo = ModelChoiceField(label="Graduate ECE Course II", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursethree = ModelChoiceField(label="Graduate ECE Course III", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursefour = ModelChoiceField(label="Graduate ECE Course IV", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    electiveone = ModelChoiceField(label="Elective I", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivetwo = ModelChoiceField(label="Elective II", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivethree = ModelChoiceField(label="Elective III", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivefour = ModelChoiceField(label="Elective IV", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    gradtechcourseone = ModelChoiceField(label="Graduate Technical Elective from ECE or other approved area Course I", queryset=Course.objects.filter(Q(category__title__iexact="Approved Technical Elective")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradtechcoursetwo = ModelChoiceField(label="Graduate Technical Elective from ECE or other approved area Course II", queryset=Course.objects.filter(Q(category__title__iexact="Approved Technical Elective")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)

    def clean(self):
        cleaned_data = super().clean()
        #counter for ECE 899: Independent Study
        indcount = 0
        #counter for Undergrad Courses
        undergrad = 0
        eceone = cleaned_data.get("gradececourseone")
        ecetwo = cleaned_data.get("gradececoursetwo")
        ecethree = cleaned_data.get("gradececoursethree")
        ecefour = cleaned_data.get("gradececoursefour")
        electiveone = cleaned_data.get("electiveone")
        electivetwo = cleaned_data.get("electivetwo")
        electivethree = cleaned_data.get("electivethree")
        electivefour = cleaned_data.get("electivefour")
        gradtechone = cleaned_data.get("gradtechcourseone")
        gradtechtwo = cleaned_data.get("gradtechcoursetwo")
        empty = False
        if ((electiveone is None) or (electivetwo is None)
        or (electivethree is None) or (electivefour is None)):
            empty = True

        #Indepdent Study Count Check
        if (empty is False):
            if (electiveone.listing == "ECE 899"):
                indcount = indcount + 1

            if (electivetwo.listing == "ECE 899"):
                indcount = indcount + 1

            if (electivethree.listing == "ECE 899"):
                indcount = indcount + 1

            if (electivefour.listing == "ECE 899"):
                indcount = indcount + 1

        #Undergraduate Course Count Check
        if (empty is False):
            if (("ECE 3" in electiveone.listing) or ("ECE 4" in electiveone.listing)):
                undergrad = undergrad +1

            if (("ECE 3" in electivetwo.listing) or ("ECE 4" in electivetwo.listing)):
                undergrad = undergrad + 1

            if (("ECE 3" in electivethree.listing) or ("ECE 4" in electivethree.listing)):
                undergrad = undergrad + 1

            if (("ECE 3" in electivefour.listing) or ("ECE 4" in electivefour.listing)):
                undergrad = undergrad + 1

        logger.error("ind count is:"+str(indcount))
        logger.error("undergrad count is:"+str(undergrad))
        logger.error("total is:"+str(undergrad+indcount))

        #Statments below check whether too many undergraduate courses along with independent studies
        if (undergrad + indcount > 2):
            self._errors['electiveone'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']
            self._errors['electivetwo'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']
            self._errors['electivethree'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']
            self._errors['electivefour'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']


        #Below checks if any fields are duplicates
        if ((eceone==ecetwo) or (eceone==ecethree) or (eceone==ecefour) or (eceone==gradtechone)
        or (eceone==gradtechtwo) or (eceone==electiveone) or (eceone==electivetwo)
        or (eceone==electivethree) or (eceone==electivefour)):
            self._errors['gradececourseone'] = [u'Graduate ECE Course I cannot be the same as any other course.']

        if ((ecetwo==ecethree) or (ecetwo==ecefour) or (ecetwo==gradtechone)
        or (ecetwo==gradtechtwo) or (ecetwo==electiveone) or (ecetwo==electivetwo)
        or (ecetwo==electivethree) or (ecetwo==electivefour)):
            self._errors['gradececoursetwo'] = [u'Graduate ECE Course II cannot be the same as any other course.']

        if ((ecethree==ecefour) or (ecethree==gradtechone) or (ecethree==gradtechtwo)
        or (ecethree==electiveone) or (ecethree==electivetwo)
        or (ecethree==electivethree) or (ecethree==electivefour)):
            self._errors['gradececoursethree'] = [u'Graduate ECE Course III cannot be the same as any other course.']

        if ((ecefour==gradtechone) or (ecefour==gradtechtwo)
        or (ecefour==electiveone) or (ecefour==electivetwo)
        or (ecefour==electivethree) or (ecefour==electivefour)):
            self._errors['gradececoursefour'] = [u'Graduate ECE Course IV cannot be the same as any other course.']

        if ((gradtechone==gradtechtwo) or (gradtechone==electiveone)
        or (gradtechone==electivetwo) or (gradtechone==electivethree)
        or (gradtechone==electivefour)):
            self._errors['gradtechcourseone'] = [u'Graduate Technical Elective I cannot be the same as any other course.']

        if ((gradtechtwo==electiveone) or (gradtechtwo==electivetwo)
        or (gradtechtwo==electivethree) or (gradtechtwo==electivefour)):
            self._errors['gradtechcoursetwo'] = [u'Graduate Technical Elective II cannot be the same as any other course.']

        if ((electiveone==electivetwo) or (electiveone==electivethree)
        or (electiveone==electivefour)):
            if (empty is False):
                if (electiveone.listing != "ECE 899"):    #
                    self._errors['electiveone'] = [u'Elective I cannot be the same as any other course.']

        if ((electivetwo==electivethree) or (electivetwo==electivefour)):
            if (empty is False):
                if (electivetwo.listing != "ECE 899"):
                    self._errors['electivetwo'] = [u'Elective II cannot be the same as any other course.']

        if (electivethree==electivefour):
            if (empty is False):
                if (electivethree.listing != "ECE 899"):
                    self._errors['electivethree'] = [u'Elective III cannot be the same as any other course.']

class MSCourseCommentForm(ModelForm):
    class Meta:
        model = MSCourseComment
        exclude = ('created_date', 'authortype', 'form')


class AdminMSCoursePOSForm(ModelForm):
    class Meta:
        model = MSCoursePOS
        exclude = ('state',)

    #Django Select2 Fields
    owner = ModelChoiceField(label="Owner", queryset=User.objects.filter(Q(user_type__icontains="MS")), widget=Select2Widget)
    gradececourseone = ModelChoiceField(label="Graduate ECE Course I", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursetwo = ModelChoiceField(label="Graduate ECE Course II", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursethree = ModelChoiceField(label="Graduate ECE Course III", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursefour = ModelChoiceField(label="Graduate ECE Course IV", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    electiveone = ModelChoiceField(label="Elective I", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivetwo = ModelChoiceField(label="Elective II", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivethree = ModelChoiceField(label="Elective III", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivefour = ModelChoiceField(label="Elective IV", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    gradtechcourseone = ModelChoiceField(label="Graduate Technical Elective from ECE or other approved area Course I", queryset=Course.objects.filter(Q(category__title__iexact="Approved Technical Elective")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradtechcoursetwo = ModelChoiceField(label="Graduate Technical Elective from ECE or other approved area Course II", queryset=Course.objects.filter(Q(category__title__iexact="Approved Technical Elective")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)


class MSProjectPOSForm(ModelForm):
    class Meta:
        model = MSProjectPOS
        exclude = ('owner', 'state')

    #Django Select2 Fields
    gradececourseone = ModelChoiceField(label="Graduate ECE Course I", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursetwo = ModelChoiceField(label="Graduate ECE Course II", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursethree = ModelChoiceField(label="Graduate ECE Course III", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursefour = ModelChoiceField(label="Graduate ECE Course IV", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    electiveone = ModelChoiceField(label="Elective I", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivetwo = ModelChoiceField(label="Elective II", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivethree = ModelChoiceField(label="Elective III", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivefour = ModelChoiceField(label="Elective IV", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivefive = ModelChoiceField(label="Elective V", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)


    def clean(self):
        cleaned_data = super().clean()
        #counter for ECE 899: Independent Study
        indcount = 0
        #counter for Undergrad Courses
        undergrad = 0

        eceone = cleaned_data.get("gradececourseone")
        ecetwo = cleaned_data.get("gradececoursetwo")
        ecethree = cleaned_data.get("gradececoursethree")
        ecefour = cleaned_data.get("gradececoursefour")
        electiveone = cleaned_data.get("electiveone")
        electivetwo = cleaned_data.get("electivetwo")
        electivethree = cleaned_data.get("electivethree")
        electivefour = cleaned_data.get("electivefour")
        electivefive = cleaned_data.get("electivefive")
        researchcourseterm = cleaned_data.get("researchcourseterm")

        empty = False
        if ((electiveone is None) or (electivetwo is None)
        or (electivethree is None) or (electivefour is None)
        or (electivefive is None)):
            empty = True

        #Indepdent Study Count Check
        if (empty is False):
            if (electiveone.listing == "ECE 899"):
                indcount = indcount + 1

            if (electivetwo.listing == "ECE 899"):
                indcount = indcount + 1

            if (electivethree.listing == "ECE 899"):
                indcount = indcount + 1

            if (electivefour.listing == "ECE 899"):
                indcount = indcount + 1

            if (electivefive.listing == "ECE 899"):
                indcount = indcount + 1

        #Undergraduate Course Count Check
        if (empty is False):
            if (("ECE 3" in electiveone.listing) or ("ECE 4" in electiveone.listing)):
                undergrad = undergrad +1

            if (("ECE 3" in electivetwo.listing) or ("ECE 4" in electivetwo.listing)):
                undergrad = undergrad + 1

            if (("ECE 3" in electivethree.listing) or ("ECE 4" in electivethree.listing)):
                undergrad = undergrad + 1

            if (("ECE 3" in electivefour.listing) or ("ECE 4" in electivefour.listing)):
                undergrad = undergrad + 1

            if (("ECE 3" in electivefive.listing) or ("ECE 4" in electivefive.listing)):
                undergrad = undergrad + 1

        logger.error("ind count is:"+str(indcount))
        logger.error("undergrad count is:"+str(undergrad))
        logger.error("total is:"+str(undergrad+indcount))

        #Statments below check whether too many undergraduate courses along with independent studies
        if (undergrad + indcount > 2):
            self._errors['electiveone'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']
            self._errors['electivetwo'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']
            self._errors['electivethree'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']
            self._errors['electivefour'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']
            self._errors['electivefive'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']


        #Below checks if any fields are duplicates
        if ((eceone==ecetwo) or (eceone==ecethree) or (eceone==ecefour)
        or (eceone==electiveone) or (eceone==electivetwo)
        or (eceone==electivethree) or (eceone==electivefour)
        or (eceone==electivefive)):
            self._errors['gradececourseone'] = [u'Graduate ECE Course I cannot be the same as any other course.']

        if ((ecetwo==ecethree) or (ecetwo==ecefour) or (ecetwo==electiveone)
        or (ecetwo==electivetwo) or (ecetwo==electivethree)
        or (ecetwo==electivefour) or (ecetwo==electivefive)):
            self._errors['gradececoursetwo'] = [u'Graduate ECE Course II cannot be the same as any other course.']

        if ((ecethree==ecefour) or (ecethree==electiveone)
        or (ecethree==electivetwo) or (ecethree==electivethree)
        or (ecethree==electivefour) or (ecethree==electivefive)):
            self._errors['gradececoursethree'] = [u'Graduate ECE Course III cannot be the same as any other course.']

        if ((ecefour==electiveone) or (ecefour==electivetwo)
        or (ecefour==electivethree) or (ecefour==electivefour)
        or (ecefour==electivefive)):
            self._errors['gradececoursefour'] = [u'Graduate ECE Course IV cannot be the same as any other course.']

        if ((electiveone==electivetwo) or (electiveone==electivethree)
        or (electiveone==electivefour) or (electiveone==electivefive)):
            if (empty is False):
                if (electiveone.listing != "ECE 899"):    #
                    self._errors['electiveone'] = [u'Elective I cannot be the same as any other course.']

        if ((electivetwo==electivethree) or (electivetwo==electivefour)
        or (electivetwo==electivefive)):
            if (empty is False):
                if (electivetwo.listing != "ECE 899"):
                    self._errors['electivetwo'] = [u'Elective II cannot be the same as any other course.']

        if ((electivethree==electivefour) or (electivethree==electivefive)):
            if (empty is False):
                if (electivethree.listing != "ECE 899"):
                    self._errors['electivethree'] = [u'Elective III cannot be the same as any other course.']

        if ((electivefour==electivefive)):
            if (empty is False):
                if (electivefour.listing != "ECE 899"):
                    self._errors['electivefour'] = [u'Elective IV cannot be the same as any other course.']


class MSProjectCommentForm(ModelForm):
    class Meta:
        model = MSProjectComment
        exclude = ('created_date', 'authortype', 'form')


class AdminMSProjectPOSForm(ModelForm):
    class Meta:
        model = MSProjectPOS
        exclude = ('state',)

    #Django Select2 Fields
    owner = ModelChoiceField(label="Owner", queryset=User.objects.filter(Q(user_type__icontains="MS")), widget=Select2Widget)
    gradececourseone = ModelChoiceField(label="Graduate ECE Course I", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursetwo = ModelChoiceField(label="Graduate ECE Course II", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursethree = ModelChoiceField(label="Graduate ECE Course III", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursefour = ModelChoiceField(label="Graduate ECE Course IV", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    electiveone = ModelChoiceField(label="Elective I", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivetwo = ModelChoiceField(label="Elective II", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivethree = ModelChoiceField(label="Elective III", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivefour = ModelChoiceField(label="Elective IV", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivefive = ModelChoiceField(label="Elective V", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)


class MSThesisPOSForm(ModelForm):
    class Meta:
        model = MSThesisPOS
        exclude = ('owner', 'state')

    #Django Select2 Fields
    gradececourseone = ModelChoiceField(label="Graduate ECE Course I", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursetwo = ModelChoiceField(label="Graduate ECE Course II", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursethree = ModelChoiceField(label="Graduate ECE Course III", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursefour = ModelChoiceField(label="Graduate ECE Course IV", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    electiveone = ModelChoiceField(label="Elective I", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivetwo = ModelChoiceField(label="Elective II", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivethree = ModelChoiceField(label="Elective III", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivefour = ModelChoiceField(label="Elective IV", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)


    def clean(self):
        cleaned_data = super().clean()
        eceone = cleaned_data.get("gradececourseone")
        ecetwo = cleaned_data.get("gradececoursetwo")
        ecethree = cleaned_data.get("gradececoursethree")
        ecefour = cleaned_data.get("gradececoursefour")
        electiveone = cleaned_data.get("electiveone")
        electivetwo = cleaned_data.get("electivetwo")
        electivethree = cleaned_data.get("electivethree")
        electivefour = cleaned_data.get("electivefour")
        researchcourseterm = cleaned_data.get("researchcourseterm")
        researchcoursetermtwo = cleaned_data.get("researchcoursetermtwo")
        empty = False
        #Counter for Independent Studies and Undergraduate Courses
        indcount = 0
        undergrad = 0
        if ((electiveone is None) or (electivetwo is None)
        or (electivethree is None) or (electivefour is None)):
            empty = True

        #Indepdent Study Count Check
        if (empty is False):
            if (electiveone.listing == "ECE 899"):
                indcount = indcount + 1

            if (electivetwo.listing == "ECE 899"):
                indcount = indcount + 1

            if (electivethree.listing == "ECE 899"):
                indcount = indcount + 1

            if (electivefour.listing == "ECE 899"):
                indcount = indcount + 1


        #Undergraduate Course Count Check
        if (empty is False):
            if (("ECE 3" in electiveone.listing) or ("ECE 4" in electiveone.listing)):
                undergrad = undergrad +1

            if (("ECE 3" in electivetwo.listing) or ("ECE 4" in electivetwo.listing)):
                undergrad = undergrad + 1

            if (("ECE 3" in electivethree.listing) or ("ECE 4" in electivethree.listing)):
                undergrad = undergrad + 1

            if (("ECE 3" in electivefour.listing) or ("ECE 4" in electivefour.listing)):
                undergrad = undergrad + 1


        logger.error("ind count is:"+str(indcount))
        logger.error("undergrad count is:"+str(undergrad))
        logger.error("total is:"+str(undergrad+indcount))

        #Statments below check whether too many undergraduate courses along with independent studies
        if (undergrad + indcount > 2):
            self._errors['electiveone'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']
            self._errors['electivetwo'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']
            self._errors['electivethree'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']
            self._errors['electivefour'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']


        #Below checks if any fields are duplicates
        if ((eceone==ecetwo) or (eceone==ecethree) or (eceone==ecefour)
        or (eceone==electiveone) or (eceone==electivetwo)
        or (eceone==electivethree) or (eceone==electivefour)):
            self._errors['gradececourseone'] = [u'Graduate ECE Course I cannot be the same as any other course.']

        if ((ecetwo==ecethree) or (ecetwo==ecefour) or (ecetwo==electiveone)
        or (ecetwo==electivetwo) or (ecetwo==electivethree)
        or (ecetwo==electivefour)):
            self._errors['gradececoursetwo'] = [u'Graduate ECE Course II cannot be the same as any other course.']

        if ((ecethree==ecefour) or (ecethree==electiveone)
        or (ecethree==electivetwo) or (ecethree==electivethree)
        or (ecethree==electivefour)):
            self._errors['gradececoursethree'] = [u'Graduate ECE Course III cannot be the same as any other course.']

        if ((ecefour==electiveone) or (ecefour==electivetwo)
        or (ecefour==electivethree) or (ecefour==electivefour)):
            self._errors['gradececoursefour'] = [u'Graduate ECE Course IV cannot be the same as any other course.']

        if ((electiveone==electivetwo) or (electiveone==electivethree)
        or (electiveone==electivefour)):
            if (empty is False):
                if (electiveone.listing != "ECE 899"):    #
                    self._errors['electiveone'] = [u'Elective I cannot be the same as any other course.']

        if ((electivetwo==electivethree) or (electivetwo==electivefour)):
            if (empty is False):
                if (electivetwo.listing != "ECE 899"):
                    self._errors['electivetwo'] = [u'Elective II cannot be the same as any other course.']

        if ((electivethree==electivefour)):
            if (empty is False):
                if (electivethree.listing != "ECE 899"):
                    self._errors['electivethree'] = [u'Elective III cannot be the same as any other course.']

class MSThesisCommentForm(ModelForm):
    class Meta:
        model = MSThesisComment
        exclude = ('created_date', 'authortype', 'form')


class AdminMSThesisPOSForm(ModelForm):
    class Meta:
        model = MSThesisPOS
        exclude = ('state',)

    #Django Select2 Fields
    owner = ModelChoiceField(label="Owner", queryset=User.objects.filter(Q(user_type__icontains="MS")), widget=Select2Widget)
    gradececourseone = ModelChoiceField(label="Graduate ECE Course I", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursetwo = ModelChoiceField(label="Graduate ECE Course II", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursethree = ModelChoiceField(label="Graduate ECE Course III", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradececoursefour = ModelChoiceField(label="Graduate ECE Course IV", queryset=Course.objects.filter((~Q(title__contains="Independent"))&Q(listing__contains="ECE")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    electiveone = ModelChoiceField(label="Elective I", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivetwo = ModelChoiceField(label="Elective II", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivethree = ModelChoiceField(label="Elective III", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivefour = ModelChoiceField(label="Elective IV", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
