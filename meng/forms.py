from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField
from django.db.models import Q #allows for complex queries
from django.utils.html import escape
from meng.models import *
from shared.models import *
from django_select2.forms import Select2Widget
import logging

logger = logging.getLogger('meng/forms.py')


class MEngPOSForm(ModelForm):
    class Meta:
        model = MEngPOS
        exclude = ('owner', 'state', )

    #Django-Ajax select Fields --> NOT IN USE
    # gradtechcourseone = make_ajax_field(MEngPOS, 'gradtechcourseone', 'gradtech', help_text=None)
    # gradtechcoursetwo = make_ajax_field(MEngPOS, 'gradtechcoursetwo', 'gradtech', help_text=None)
    # electiveone = make_ajax_field(MEngPOS, 'electiveone', 'elective', help_text=None)
    # electivetwo = make_ajax_field(MEngPOS, 'electivetwo', 'elective', help_text=None)
    # electivethree = make_ajax_field(MEngPOS, 'electivethree', 'elective', help_text=None)

    #Django select2 Fields
    coreclassone = ModelChoiceField(label="Core Industry Prep Course I", queryset=Course.objects.filter(Q(listing__iexact="MENG  540")), widget=Select2Widget)
    coreclasstwo = ModelChoiceField(label="Core Industry Prep Course II", queryset=Course.objects.filter(Q(listing__iexact="MENG  570")), widget=Select2Widget)
    gradtechcourseone = ModelChoiceField(label="Graduate Technical Elective I", queryset=Course.objects.filter(Q(category__title__iexact="Approved Technical Elective")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradtechcoursetwo = ModelChoiceField(label="Graduate Technical Elective II", queryset=Course.objects.filter(Q(category__title__iexact="Approved Technical Elective")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    techcourseone = ModelChoiceField(label="ECE Technical Course I from Concentration Area", queryset=Course.objects.all(), widget=Select2Widget)
    techcoursetwo = ModelChoiceField(label="ECE Technical Course II from Concentration Area", queryset=Course.objects.all(), widget=Select2Widget)
    techcoursethree = ModelChoiceField(label="ECE Technical Course III from Concentration Area", queryset=Course.objects.all(), widget=Select2Widget)
    electiveone = ModelChoiceField(label="Elective I", queryset=Course.objects.filter(Q(category__title__iexact="Elective")), widget=Select2Widget)
    electivetwo = ModelChoiceField(label="Elective II", queryset=Course.objects.filter(Q(category__title__iexact="Elective")), widget=Select2Widget)
    electivethree = ModelChoiceField(label="Elective III", queryset=Course.objects.filter(Q(category__title__iexact="Elective")), widget=Select2Widget)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['techcourseone'].queryset = Course.objects.none()
        self.fields['techcoursetwo'].queryset = Course.objects.none()
        self.fields['techcoursethree'].queryset = Course.objects.none()

        if 'concentration' in self.data:
            try:
                concentration_id = int(self.data.get('concentration'))
                concentration_entry = Concentration.objects.get(pk=concentration_id)
                self.fields['techcourseone'].queryset = Course.objects.filter(concentration=concentration_entry).order_by('listing', 'title')
                self.fields['techcoursetwo'].queryset = Course.objects.filter(concentration=concentration_entry).order_by('listing', 'title')
                self.fields['techcoursethree'].queryset = Course.objects.filter(concentration=concentration_entry).order_by('listing', 'title')

            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Concentration queryset
        elif self.instance.pk:
            self.fields['techcourseone'].queryset = self.instance.concentration.course_set.order_by('listing', 'title')
            self.fields['techcoursetwo'].queryset = self.instance.concentration.course_set.order_by('listing', 'title')
            self.fields['techcoursethree'].queryset = self.instance.concentration.course_set.order_by('listing', 'title')


    def clean(self):
        cleaned_data = super().clean()
        coreclassone = cleaned_data.get("coreone")
        coreclasstwo = cleaned_data.get("coretwo")
        techone = cleaned_data.get("techcourseone")
        techtwo = cleaned_data.get("techcoursetwo")
        techthree = cleaned_data.get("techcoursethree")
        gradtechone = cleaned_data.get("gradtechcourseone")
        gradtechtwo = cleaned_data.get("gradtechcoursetwo")
        electiveone = cleaned_data.get("electiveone")
        electivetwo = cleaned_data.get("electivetwo")
        electivethree = cleaned_data.get("electivethree")
        indcount = 0
        undergrad = 0


        empty = False
        if ((electiveone is None) or (electivetwo is None)
        or (electivethree is None)):
            empty = True


        # #Independent Study Counting
        if (empty is False):
            if (electiveone.listing == "ECE 899"):
                indcount = indcount + 1
                logger.error("elective one makes ind count:"+str(indcount))

            if (electivetwo.listing == "ECE 899"):
                indcount = indcount + 1
                logger.error("elective two makes ind count:"+str(indcount))

            if (electivethree.listing == "ECE 899"):
                indcount = indcount + 1
                logger.error("elective three makes ind count:"+str(indcount))

        # #Undergraduate Study Counting
        if (empty is False):
            if (("ECE 3" in electiveone.listing) or ("ECE 4" in electiveone.listing)):
                undergrad = undergrad +1
                logger.error("elective one makes undergrad count:"+str(undergrad))

            if (("ECE 3" in electivetwo.listing) or ("ECE 4" in electivetwo.listing)):
                undergrad = undergrad + 1
                logger.error("elective two makes undergrad count:"+str(undergrad))

            if (("ECE 3" in electivethree.listing) or ("ECE 4" in electivethree.listing)):
                undergrad = undergrad + 1
                logger.error("elective three makes undergrad count:"+str(undergrad))

        logger.error("ind count is:"+str(indcount))
        logger.error("undergrad count is:"+str(undergrad))
        logger.error("total is:"+str(undergrad+indcount))


        #Independent Study/Undergraduate Course Count Check
        if (undergrad + indcount > 2):
            # raise ValidationError("Students can count at most two 300/400 level classes, two Independent Studies" +
            # " or one Independent Study and one 300/400 level class in combination towards their degree.")
            self._errors['electiveone'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']
            self._errors['electivetwo'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']
            self._errors['electivethree'] = [u'At most two undergraduate courses, two independent study courses, or one of each are permitted.']


        #Duplicate Checks
        if ((coreclassone==electiveone) or (coreclassone==electivetwo) or (coreclassone==electivethree)):
            self._errors['coreone'] = [u'Core Industry Prep Course I cannot be counted twice.']

        if ((coreclasstwo==electiveone) or (coreclasstwo==electivetwo) or (coreclasstwo==electivethree)):
            self._errors['coretwo'] = [u'Core Industry Prep Course II cannot be counted twice.']

        if ((techone==techtwo) or (techone==techthree) or (techone==gradtechone)
        or (techone==gradtechtwo) or (techone==electiveone) or (techone==electivetwo)
        or (techone==electivethree)):
            self._errors['techcourseone'] = [u'ECE Technical Course I cannot be the same as any other course.']

        if ((techtwo==techthree) or (techtwo==gradtechone) or (techtwo==gradtechtwo) or
        (techtwo==electiveone) or (techtwo==electivetwo) or (techtwo==electivethree)):
            self._errors['techcoursetwo'] = [u'ECE Technical Course II cannot be the same as any other course.']

        if ((techthree==gradtechone) or (techthree==gradtechtwo) or (techthree==electiveone)
        or (techthree==electivetwo) or (techthree==electivethree)):
            self._errors['techcoursethree'] = [u'ECE Technical Course III cannot be the same as any other course.']

        if ((gradtechone==gradtechtwo) or (gradtechone==electiveone) or (gradtechone==electivetwo) or
        (gradtechone==electivethree)):
            self._errors['gradtechcourseone'] = [u'Graduate Technical Elective I cannot be the same as any other course.']

        if ((gradtechtwo==electiveone) or (gradtechtwo==electivetwo) or (gradtechtwo==electivethree)):
            self._errors['gradtechcoursetwo'] = [u'Graduate Technical Elective II cannot be the same as any other course.']

        if ((electiveone==electivetwo) or (electiveone==electivethree)):
            if (empty is False):
                if (electiveone.listing != "ECE 899"):    #
                    self._errors['electiveone'] = [u'Elective I cannot be the same as any other course.']

        if (electivetwo==electivethree):
            if (empty is False):
                if (electivetwo.listing != "ECE 899"):
                    self._errors['electivetwo'] = [u'Elective II cannot be the same as any other course.']


class MEngCommentForm(ModelForm):
    class Meta:
        model = MEngComment
        exclude = ('created_date', 'authortype', 'form')

class AdminMEngPOSForm(ModelForm):
    class Meta:
        model = MEngPOS
        exclude = ('state', )

    #1 corresponds to MEng
    owner = ModelChoiceField(label="Owner", queryset=User.objects.filter(Q(user_type__icontains="MEng")), widget=Select2Widget)
    coreclassone = ModelChoiceField(label="Core Industry Prep Course I", queryset=Course.objects.filter(Q(listing__iexact="MENG  540")), widget=Select2Widget)
    coreclasstwo = ModelChoiceField(label="Core Industry Prep Course II", queryset=Course.objects.filter(Q(listing__iexact="MENG  570")), widget=Select2Widget)
    gradtechcourseone = ModelChoiceField(label="Graduate Technical Elective I", queryset=Course.objects.filter(Q(category__title__iexact="Approved Technical Elective")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    gradtechcoursetwo = ModelChoiceField(label="Graduate Technical Elective II", queryset=Course.objects.filter(Q(category__title__iexact="Approved Technical Elective")&(Q(listing__contains="5")|Q(listing__contains="6")|Q(listing__contains="7")|Q(listing__contains="8")|Q(listing__contains="9"))), widget=Select2Widget)
    techcourseone = ModelChoiceField(label="ECE Technical Course I from Concentration Area", queryset=Course.objects.all(), widget=Select2Widget)
    techcoursetwo = ModelChoiceField(label="ECE Technical Course II from Concentration Area", queryset=Course.objects.all(), widget=Select2Widget)
    techcoursethree = ModelChoiceField(label="ECE Technical Course III from Concentration Area", queryset=Course.objects.all(), widget=Select2Widget)
    electiveone = ModelChoiceField(label="Elective I", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivetwo = ModelChoiceField(label="Elective II", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)
    electivethree = ModelChoiceField(label="Elective III", queryset=Course.objects.filter(Q(category__title__exact="Elective")), widget=Select2Widget)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['techcourseone'].queryset = Course.objects.none()
        self.fields['techcoursetwo'].queryset = Course.objects.none()
        self.fields['techcoursethree'].queryset = Course.objects.none()

        if 'concentration' in self.data:
            try:
                concentration_id = int(self.data.get('concentration'))
                concentration_entry = Concentration.objects.get(pk=concentration_id)
                self.fields['techcourseone'].queryset = Course.objects.filter(listing__contains="ECE").order_by('listing', 'title')
                self.fields['techcoursetwo'].queryset = Course.objects.filter(listing__contains="ECE").order_by('listing', 'title')
                self.fields['techcoursethree'].queryset = Course.objects.filter(listing__contains="ECE").order_by('listing', 'title')

            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Concentration queryset
        elif self.instance.pk:
            self.fields['techcourseone'].queryset = self.instance.concentration.course_set.order_by('listing', 'title')
            self.fields['techcoursetwo'].queryset = self.instance.concentration.course_set.order_by('listing', 'title')
            self.fields['techcoursethree'].queryset = self.instance.concentration.course_set.order_by('listing', 'title')
