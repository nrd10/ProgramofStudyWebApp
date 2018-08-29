from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.forms.utils import ErrorList
from ms.models import *
from ms.forms import *
from shared.models import *
from django import forms
from django.contrib.auth.decorators import permission_required
from ms.filters import *
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, send_mail
from django.utils.html import strip_tags
from django.template.loader import get_template, render_to_string
from django.template import Context
# Create your views here.
class MSCourseListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'ms.MSc_Student_View'
    model = MSCoursePOS
    context_object_name = 'form_list'
    template_name = 'list.html'
    paginate_by = 10

    def get_queryset(self):
        return MSCoursePOS.objects.filter(owner=self.request.user)

    def get_approved(self):
        return MSCoursePOS.objects.filter(Q(owner=self.request.user)&Q(state="Approved"))

    def get_rejected(self):
        return MSCoursePOS.objects.filter(Q(owner=self.request.user)&(Q(state="AdvisorRejected")|Q(state="DGSRejected")))

    def get_pending(self):
        return MSCoursePOS.objects.filter(Q(owner=self.request.user)&(Q(state="AdvisorPending")|Q(state="DGSPending")))

    def get_context_data(self, **kwargs):
        context = super(MSCourseListView, self).get_context_data(**kwargs)
        context['approvedcount'] = self.get_approved().count()
        context['rejectedcount'] = self.get_rejected().count()
        context['pendingcount'] = self.get_pending().count()
        context['list'] = "MSc"
        context['usertype'] = "MS"

        return context


class MSCourseDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'ms.MSc_Student_View'
    model = MSCoursePOS
    template_name = 'MSCourse_detail.html'

    def get_object(self):
        """Returns the MSCoursePOS instance that the view displays"""
        owner = MSCoursePOS.objects.filter(owner=self.request.user)
        object = MSCoursePOS.objects.get(pk=self.kwargs.get("pk"))
        if (object.owner == self.request.user):
            return object
        else:
            raise PermissionDenied


    def get_context_data(self, **kwargs):
        context = super(MSCourseDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "MS"
        return context


class MSCourseUpdateView(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    permission_required = 'ms.MSc_Student_View'
    model = MSCoursePOS
    form_class = MSCoursePOSForm
    template_name_suffix = '_msc_form'

    def get_object(self):
        """Returns the MEngPOS instance that the view displays"""
        owner = MSCoursePOS.objects.filter(owner=self.request.user)
        object = MSCoursePOS.objects.get(pk=self.kwargs.get("pk"))
        if (object.owner == self.request.user):
            return object
        else:
            raise PermissionDenied

    def dispatch(self, request, *args, **kwargs):
        object = MSCoursePOS.objects.get(pk=self.kwargs.get("pk"))
        if ((object.state == "AdvisorPending") or (object.state == "DGSPending") or (object.state == "Approved")):
            messages.add_message(self.request, messages.ERROR, "Students can only update forms when they are " \
            "rejected.")
            return redirect('mscourse-detail', pk=self.kwargs.get("pk"))

        else:
            return super(MSCourseUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        x =  MSCoursePOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        y =  MSProjectPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        z =  MSThesisPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        if (len(x) + len(y) + len(z) > 0):
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
            u'Students may only resubmit a form if they do not have a current form under review.'
            ])
            return self.form_invalid(form)

        user = self.request.user
        form.instance.owner = user
        form.instance.state = "AdvisorPending"
        return super(MSCourseUpdateView, self).form_valid(form)


class MSCourseAdvisorListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'ms.MSc_Advisor_View'
    model = MSCoursePOS
    context_object_name = 'form_list'
    template_name = 'list.html'
    paginate_by = 10

    def get_queryset(self):
        return MSCoursePOS.objects.filter(Q(owner__advisor=self.request.user)&Q(state="AdvisorPending"))

    def get_context_data(self, **kwargs):
        context = super(MSCourseAdvisorListView, self).get_context_data(**kwargs)
        context['advisorcount'] = self.get_queryset().count()
        context['list'] = "MSc"
        context['usertype'] = "Advisor"
        return context

class MSCourseAdvisorDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'ms.MSc_Advisor_View'
    model = MSCoursePOS
    template_name = 'MSCourse_detail.html'

    def get_object(self):
        """Returns the MSCoursePOS instance that the view displays"""
        object = MSCoursePOS.objects.get(pk=self.kwargs.get("pk"))
        ##Restrict Advisor View --> Unable to see old form if DGSRejected or Approved
        if ((object.state == "DGSRejected") or (object.state == "Approved")):
            raise PermissionDenied
        if (object.owner.advisor == self.request.user):
            return object
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(MSCourseAdvisorDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "Advisor"
        return context



class MSCourseAdvisorHistoryView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'ms.MSc_Advisor_View'
    model = MSCoursePOS
    context_object_name = 'form_list'
    template_name = 'history.html'
    paginate_by = 10

    def get_queryset(self):
        return MSCoursePOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="AdvisorRejected")|Q(state="DGSPending")))

    def get_approved(self):
        return MSCoursePOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="DGSPending")))

    def get_rejected(self):
        return MSCoursePOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="AdvisorRejected")))

    def get_context_data(self, **kwargs):
        context = super(MSCourseAdvisorHistoryView, self).get_context_data(**kwargs)
        context['advisorapproved'] = self.get_approved().count()
        context['advisorrejected'] = self.get_rejected().count()
        context['history'] = "MSc"
        return context


class MSCourseDGSListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'ms.MSc_DGS_View'
    model = MSCoursePOS
    context_object_name = 'form_list'
    template_name = 'dgslist.html'
    paginate_by = 10

    def get_queryset(self):
        return MSCoursePOS.objects.filter(Q(state="DGSPending"))

    def get_context_data(self, **kwargs):
        context = super(MSCourseDGSListView, self).get_context_data(**kwargs)
        context['dgscount'] = self.get_queryset().count()
        context['list'] = "MSc"
        return context

class MSCourseDGSDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'ms.MSc_DGS_View'
    model = MSCoursePOS
    template_name = 'MSCourse_detail.html'


    def get_context_data(self, **kwargs):
        context = super(MSCourseDGSDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "DGS"
        return context

class MSCourseDGSHistoryView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'ms.MSc_DGS_View'
    model = MSCoursePOS
    context_object_name = 'form_list'
    template_name = 'history.html'
    paginate_by = 10

    def get_queryset(self):
        return MSCoursePOS.objects.filter(Q(state="Approved")|Q(state="DGSRejected"))

    def get_rejected(self):
        return MSCoursePOS.objects.filter(Q(state="DGSRejected"))

    def get_approved(self):
        return MSCoursePOS.objects.filter(Q(state="Approved"))

    def get_context_data(self, **kwargs):
        context = super(MSCourseDGSHistoryView, self).get_context_data(**kwargs)
        context['dgsrejected'] = self.get_rejected().count()
        context['dgsapproved'] = self.get_approved().count()
        context['history'] = "MSc"
        return context


class AdminMSCourseDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'ms.MSc_Admin_View'
    model = MSCoursePOS
    template_name = 'MSCourse_detail.html'


    def get_context_data(self, **kwargs):
        context = super(AdminMSCourseDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "Administrator"
        return context

class MSProjectListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'ms.MSp_Student_View'
    model = MSProjectPOS
    context_object_name = 'form_list'
    template_name = 'list.html'
    paginate_by = 10

    def get_queryset(self):
        return MSProjectPOS.objects.filter(owner=self.request.user)

    def get_approved(self):
        return MSProjectPOS.objects.filter(Q(owner=self.request.user)&Q(state="Approved"))

    def get_rejected(self):
        return MSProjectPOS.objects.filter(Q(owner=self.request.user)&(Q(state="AdvisorRejected")|Q(state="DGSRejected")))

    def get_pending(self):
        return MSProjectPOS.objects.filter(Q(owner=self.request.user)&(Q(state="AdvisorPending")|Q(state="DGSPending")))

    def get_context_data(self, **kwargs):
        context = super(MSProjectListView, self).get_context_data(**kwargs)
        context['approvedcount'] = self.get_approved().count()
        context['rejectedcount'] = self.get_rejected().count()
        context['pendingcount'] = self.get_pending().count()
        context['list'] = "MSp"
        context['usertype'] = "MS"
        return context


class MSProjectDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'ms.MSp_Student_View'
    model = MSProjectPOS
    template_name = 'MSProject_detail.html'

    def get_object(self):
        """Returns the MSProjectPOS instance that the view displays"""
        owner = MSProjectPOS.objects.filter(owner=self.request.user)
        object = MSProjectPOS.objects.get(pk=self.kwargs.get("pk"))
        if (object.owner == self.request.user):
            return object
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(MSProjectDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "MS"
        return context


class MSProjectUpdateView(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    permission_required = 'ms.MSp_Student_View'
    model = MSProjectPOS
    form_class = MSProjectPOSForm
    template_name_suffix = '_msp_form'

    def get_object(self):
        """Returns the MEngPOS instance that the view displays"""
        owner = MSProjectPOS.objects.filter(owner=self.request.user)
        object = MSProjectPOS.objects.get(pk=self.kwargs.get("pk"))
        if (object.owner == self.request.user):
            return object
        else:
            raise PermissionDenied

    def dispatch(self, request, *args, **kwargs):
        object = MSProjectPOS.objects.get(pk=self.kwargs.get("pk"))
        if ((object.state == "AdvisorPending") or (object.state == "DGSPending") or (object.state == "Approved")):
            messages.add_message(self.request, messages.ERROR, "Students can only update forms when they are " \
            "rejected.")
            return redirect('msproject-detail', pk=self.kwargs.get("pk"))

        else:
            return super(MSProjectUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        x =  MSCoursePOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        y =  MSProjectPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        z =  MSThesisPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        if (len(x) + len(y) + len(z) > 0):
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
            u'Students may only resubmit a form if they do not have a current form under review.'
            ])
            return self.form_invalid(form)

        user = self.request.user
        form.instance.owner = user
        form.instance.state = "AdvisorPending"
        return super(MSProjectUpdateView, self).form_valid(form)

class MSProjectAdvisorListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'ms.MSp_Advisor_View'
    model = MSProjectPOS
    context_object_name = 'form_list'
    template_name = 'list.html'
    paginate_by = 10

    def get_queryset(self):
        return MSProjectPOS.objects.filter(Q(owner__advisor=self.request.user)&Q(state="AdvisorPending"))

    def get_context_data(self, **kwargs):
        context = super(MSProjectAdvisorListView, self).get_context_data(**kwargs)
        context['advisorcount'] = self.get_queryset().count()
        context['list'] = "MSp"
        context['usertype'] = "Advisor"
        return context

class MSProjectAdvisorDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'ms.MSp_Advisor_View'
    model = MSProjectPOS
    template_name = 'MSProject_detail.html'

    def get_object(self):
        """Returns the MSProjectPOS instance that the view displays"""
        object = MSProjectPOS.objects.get(pk=self.kwargs.get("pk"))
        ##Restrict Advisor View --> Unable to see old form if DGSRejected or Approved
        if ((object.state == "DGSRejected") or (object.state == "Approved")):
            raise PermissionDenied
        if (object.owner.advisor == self.request.user):
            return object
        else:
            raise PermissionDenied


    def get_context_data(self, **kwargs):
        context = super(MSProjectAdvisorDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "Advisor"
        return context

class MSProjectAdvisorHistoryView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'ms.MSp_Advisor_View'
    model = MSProjectPOS
    context_object_name = 'form_list'
    template_name = 'history.html'
    paginate_by = 10

    def get_queryset(self):
        return MSProjectPOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="AdvisorRejected")|Q(state="DGSPending")))

    def get_approved(self):
        return MSProjectPOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="DGSPending")))

    def get_rejected(self):
        return MSProjectPOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="AdvisorRejected")))

    def get_context_data(self, **kwargs):
        context = super(MSProjectAdvisorHistoryView, self).get_context_data(**kwargs)
        context['advisorapproved'] = self.get_approved().count()
        context['advisorrejected'] = self.get_rejected().count()
        context['history'] = "MSp"
        return context


class MSProjectDGSListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'ms.MSp_DGS_View'
    model = MSProjectPOS
    context_object_name = 'form_list'
    template_name = 'dgslist.html'
    paginate_by = 10

    def get_queryset(self):
        return MSProjectPOS.objects.filter(Q(state="DGSPending"))

    def get_context_data(self, **kwargs):
        context = super(MSProjectDGSListView, self).get_context_data(**kwargs)
        context['dgscount'] = self.get_queryset().count()
        context['list'] = "MSp"
        return context

class MSProjectDGSDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'ms.MSp_DGS_View'
    model = MSProjectPOS
    template_name = 'MSProject_dgs_detail.html'


    def get_context_data(self, **kwargs):
        context = super(MSProjectDGSDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "DGS"
        return context

class MSProjectDGSHistoryView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'ms.MSp_DGS_View'
    model = MSProjectPOS
    context_object_name = 'form_list'
    template_name = 'history.html'
    paginate_by = 10

    def get_queryset(self):
        return MSProjectPOS.objects.filter(Q(state="Approved")|Q(state="DGSRejected"))

    def get_rejected(self):
        return MSProjectPOS.objects.filter(Q(state="DGSRejected"))

    def get_approved(self):
        return MSProjectPOS.objects.filter(Q(state="Approved"))

    def get_context_data(self, **kwargs):
        context = super(MSProjectDGSHistoryView, self).get_context_data(**kwargs)
        context['dgsrejected'] = self.get_rejected().count()
        context['dgsapproved'] = self.get_approved().count()
        context['history'] = "MSp"
        return context

class AdminMSProjectDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'ms.MSp_Admin_View'
    model = MSProjectPOS
    template_name = 'MSProject_detail.html'


    def get_context_data(self, **kwargs):
        context = super(AdminMSProjectDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "Administrator"
        return context


class MSThesisListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'ms.MSt_Student_View'
    model = MSThesisPOS
    context_object_name = 'form_list'
    template_name = 'list.html'
    paginate_by = 10

    def get_queryset(self):
        return MSThesisPOS.objects.filter(owner=self.request.user)

    def get_approved(self):
        return MSThesisPOS.objects.filter(Q(owner=self.request.user)&Q(state="Approved"))

    def get_rejected(self):
        return MSThesisPOS.objects.filter(Q(owner=self.request.user)&(Q(state="AdvisorRejected")|Q(state="DGSRejected")))

    def get_pending(self):
        return MSThesisPOS.objects.filter(Q(owner=self.request.user)&(Q(state="AdvisorPending")|Q(state="DGSPending")))

    def get_context_data(self, **kwargs):
        context = super(MSThesisListView, self).get_context_data(**kwargs)
        context['approvedcount'] = self.get_approved().count()
        context['rejectedcount'] = self.get_rejected().count()
        context['pendingcount'] = self.get_pending().count()
        context['list'] = "MSt"
        context['usertype'] = "MS"
        return context


class MSThesisDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'ms.MSt_Student_View'
    model = MSThesisPOS
    template_name = 'MSThesis_detail.html'


    def get_object(self):
        """Returns the MSThesisPOS instance that the view displays"""
        owner = MSThesisPOS.objects.filter(owner=self.request.user)
        object = MSThesisPOS.objects.get(pk=self.kwargs.get("pk"))
        if (object.owner == self.request.user):
            return object
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(MSThesisDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "MS"
        return context

class MSThesisUpdateView(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    permission_required = 'ms.MSt_Student_View'
    model = MSThesisPOS
    form_class = MSThesisPOSForm
    template_name_suffix = '_mst_form'

    def get_object(self):
        """Returns the MEngPOS instance that the view displays"""
        owner = MSThesisPOS.objects.filter(owner=self.request.user)
        object = MSThesisPOS.objects.get(pk=self.kwargs.get("pk"))
        if (object.owner == self.request.user):
            return object
        else:
            raise PermissionDenied

    def dispatch(self, request, *args, **kwargs):
        object = MSThesisPOS.objects.get(pk=self.kwargs.get("pk"))
        if ((object.state == "AdvisorPending") or (object.state == "DGSPending") or (object.state == "Approved")):
            messages.add_message(self.request, messages.ERROR, "Students can only update forms when they are " \
            "rejected.")
            return redirect('msthesis-detail', pk=self.kwargs.get("pk"))

        else:
            return super(MSThesisUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        x =  MSCoursePOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        y =  MSProjectPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        z =  MSThesisPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))

        if (len(x) + len(y) + len(z) > 0):
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
            u'Students may only resubmit a form if they do not have a current form under review.'
            ])
            return self.form_invalid(form)

        user = self.request.user
        form.instance.owner = user
        form.instance.state = "AdvisorPending"
        return super(MSThesisUpdateView, self).form_valid(form)


class MSThesisAdvisorListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'ms.MSt_Advisor_View'
    model = MSThesisPOS
    context_object_name = 'form_list'
    template_name = 'list.html'
    paginate_by = 10

    def get_queryset(self):
        return MSThesisPOS.objects.filter(Q(owner__advisor=self.request.user)&Q(state="AdvisorPending"))

    def get_context_data(self, **kwargs):
        context = super(MSThesisAdvisorListView, self).get_context_data(**kwargs)
        context['advisorcount'] = self.get_queryset().count()
        context['list'] = "MSt"
        context['usertype'] = "Advisor"
        return context

class MSThesisAdvisorDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'ms.MSt_Advisor_View'
    model = MSThesisPOS
    template_name = 'MSThesis_detail.html'

    def get_object(self):
        """Returns the MSThesisPOS instance that the view displays"""
        object = MSThesisPOS.objects.get(pk=self.kwargs.get("pk"))
        ##Restrict Advisor View --> Unable to see old form if DGSRejected or Approved
        if ((object.state == "DGSRejected") or (object.state == "Approved")):
            raise PermissionDenied
        if (object.owner.advisor == self.request.user):
            return object
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(MSThesisAdvisorDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "Advisor"
        return context

class MSThesisAdvisorHistoryView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'ms.MSt_Advisor_View'
    model = MSThesisPOS
    context_object_name = 'form_list'
    template_name = 'history.html'
    paginate_by = 10

    def get_queryset(self):
        return MSThesisPOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="AdvisorRejected")|Q(state="DGSPending")))

    def get_approved(self):
        return MSThesisPOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="DGSPending")))

    def get_rejected(self):
        return MSThesisPOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="AdvisorRejected")))

    def get_context_data(self, **kwargs):
        context = super(MSThesisAdvisorHistoryView, self).get_context_data(**kwargs)
        context['advisorapproved'] = self.get_approved().count()
        context['advisorrejected'] = self.get_rejected().count()
        context['history'] = "MSt"
        return context


class MSThesisDGSListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'ms.MSt_DGS_View'
    model = MSThesisPOS
    context_object_name = 'form_list'
    template_name = 'dgslist.html'
    paginate_by = 10

    def get_queryset(self):
        return MSThesisPOS.objects.filter(Q(state="DGSPending"))

    def get_context_data(self, **kwargs):
        context = super(MSThesisDGSListView, self).get_context_data(**kwargs)
        context['dgscount'] = self.get_queryset().count()
        context['list'] = "MSt"
        return context

class MSThesisDGSDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'ms.MSt_DGS_View'
    model = MSThesisPOS
    template_name = 'MSThesis_detail.html'


    def get_context_data(self, **kwargs):
        context = super(MSThesisDGSDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "DGS"
        return context

class MSThesisDGSHistoryView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'ms.MSt_DGS_View'
    model = MSThesisPOS
    context_object_name = 'form_list'
    template_name = 'history.html'
    paginate_by = 10

    def get_queryset(self):
        return MSThesisPOS.objects.filter(Q(state="Approved")|Q(state="DGSRejected"))

    def get_rejected(self):
        return MSThesisPOS.objects.filter(Q(state="DGSRejected"))

    def get_approved(self):
        return MSThesisPOS.objects.filter(Q(state="Approved"))

    def get_context_data(self, **kwargs):
        context = super(MSThesisDGSHistoryView, self).get_context_data(**kwargs)
        context['dgsrejected'] = self.get_rejected().count()
        context['dgsapproved'] = self.get_approved().count()
        context['history'] = "MSt"
        return context


class AdminMSThesisDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'ms.MSt_Admin_View'
    model = MSThesisPOS
    template_name = 'MSThesis_detail.html'


    def get_context_data(self, **kwargs):
        context = super(AdminMSThesisDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "Administrator"
        return context

class MSCoursePOSCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'ms.MSc_Student_Create'
    model = MSCoursePOS
    form_class = MSCoursePOSForm
    template_name_suffix = '_msc_form'

    def form_valid(self, form):
        # Sets the owner as the person who created the form
        x =  MSCoursePOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        y =  MSProjectPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        z =  MSThesisPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))

        if (len(x) + len(y) + len(z) > 0):
            # raise ValidationError("Students may only submit a new form if they do not have a current form under review.")
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
            u'Students may only submit a new form if they do not have a current form under review.'
            ])
            return self.form_invalid(form)

        user = self.request.user
        form.instance.owner = user
        form.instance.state = "AdvisorPending"
        return super(MSCoursePOSCreate, self).form_valid(form)


class AdminMSCoursePOSCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'ms.MSc_Admin_Create'
    model = MSCoursePOS
    form_class = AdminMSCoursePOSForm
    template_name_suffix = '_msc_form'
    def form_valid(self, form):
        form.instance.state = "AdvisorPending"
        return super(AdminMSCoursePOSCreate, self).form_valid(form)

    def get_success_url(self):
        """
        Returns the supplied URL.
        """
        if self.success_url:
            url = self.success_url % self.object.__dict__
        else:
            try:
                url = self.object.get_admin_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url

    def get_context_data(self, **kwargs):
        context = super(AdminMSCoursePOSCreate, self).get_context_data(**kwargs)
        context['usertype'] = "Administrator"
        return context

class MSProjectPOSCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'ms.MSp_Student_Create'
    model = MSProjectPOS
    form_class = MSProjectPOSForm
    template_name_suffix = '_msp_form'

    def form_valid(self, form):
        # Sets the owner as the person who created the form
        x =  MSCoursePOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        y =  MSProjectPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        z =  MSThesisPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))

        if (len(x) + len(y) + len(z) > 0):
            # raise ValidationError("Students may only submit a new form if they do not have a current form under review.")
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
            u'Students may only submit a new form if they do not have a current form under review.'
            ])
            return self.form_invalid(form)

        user = self.request.user
        form.instance.owner = user
        form.instance.state = "AdvisorPending"
        return super(MSProjectPOSCreate, self).form_valid(form)


class AdminMSProjectPOSCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'ms.MSp_Admin_Create'
    model = MSProjectPOS
    form_class = AdminMSProjectPOSForm
    template_name_suffix = '_msp_form'
    def form_valid(self, form):
        form.instance.state = "AdvisorPending"
        return super(AdminMSProjectPOSCreate, self).form_valid(form)

    def get_success_url(self):
        """
        Returns the supplied URL.
        """
        if self.success_url:
            url = self.success_url % self.object.__dict__
        else:
            try:
                url = self.object.get_admin_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url

    def get_context_data(self, **kwargs):
        context = super(AdminMSProjectPOSCreate, self).get_context_data(**kwargs)
        context['usertype'] = "Administrator"
        return context


class MSThesisPOSCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'ms.MSt_Student_Create'
    model = MSThesisPOS
    form_class = MSThesisPOSForm
    template_name_suffix = '_mst_form'

    def form_valid(self, form):
        # Sets the owner as the person who created the form
        x =  MSCoursePOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        y =  MSProjectPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        z =  MSThesisPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        if (len(x) + len(y) + len(z) > 0):
            # raise ValidationError("Students may only submit a new form if they do not have a current form under review.")
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
            u'Students may only submit a new form if they do not have a current form under review.'
            ])
            return self.form_invalid(form)

        user = self.request.user
        form.instance.owner = user
        form.instance.state = "AdvisorPending"
        return super(MSThesisPOSCreate, self).form_valid(form)


class AdminMSThesisPOSCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'ms.MSt_Admin_Create'
    model = MSThesisPOS
    form_class = AdminMSThesisPOSForm
    template_name_suffix = '_mst_form'
    def form_valid(self, form):
        form.instance.state = "AdvisorPending"
        return super(AdminMSThesisPOSCreate, self).form_valid(form)

    def get_success_url(self):
        """
        Returns the supplied URL.
        """
        if self.success_url:
            url = self.success_url % self.object.__dict__
        else:
            try:
                url = self.object.get_admin_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url


    def get_context_data(self, **kwargs):
        context = super(AdminMSThesisPOSCreate, self).get_context_data(**kwargs)
        context['usertype'] = "Administrator"
        return context

#Allows Admin to search for forms: HISTORY PAGE
@permission_required('ms.MSc_Admin_View')
def AdminMSCoursePOSsearch(request):
    posfilter = MSCoursePOSFilter(request.GET, queryset=MSCoursePOS.objects.all())
    pos_list = posfilter.qs
    type = "MSCoursePOS"
    usertype = "Administrator"
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
         'users':users, 'type':type, 'page':page, 'search':'first',
         'usertype':usertype,}
    # return render(request, 'search.html', {'filter': posfilter})
    return render(request, 'search.html', args)


#Allows Admin to search for forms: HISTORY PAGE
@permission_required('ms.MSp_Admin_View')
def AdminMSProjectPOSsearch(request):
    posfilter = MSProjectPOSFilter(request.GET, queryset=MSProjectPOS.objects.all())
    pos_list = posfilter.qs
    type = "MSProjectPOS"
    usertype = "Administrator"
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
         'users':users, 'type':type, 'page':page, 'search':'first',
         'usertype':usertype,}
    # return render(request, 'search.html', {'filter': posfilter})
    return render(request, 'search.html', args)



#Allows Admin to search for forms: HISTORY PAGE
@permission_required('ms.MSt_Admin_View')
def AdminMSThesisPOSsearch(request):
    posfilter = MSThesisPOSFilter(request.GET, queryset=MSThesisPOS.objects.all())
    pos_list = posfilter.qs
    type = "MSThesisPOS"
    usertype = "Administrator"
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
         'users':users, 'type':type, 'page':page, 'search':'first',
         'usertype':usertype,}
    # return render(request, 'search.html', {'filter': posfilter})
    return render(request, 'search.html', args)


#MSCourse Function to Delete Forms
@permission_required('ms.MSc_Admin_View')
def mscoursedelete(request, form_id):
    form = get_object_or_404(MSCoursePOS, pk=form_id)
    form.delete()
    return redirect('index')


#MSProject Function to Delete Forms
@permission_required('ms.MSp_Admin_View')
def msprojectdelete(request, form_id):
    form = get_object_or_404(MSProjectPOS, pk=form_id)
    form.delete()
    return redirect('index')


#MSThesis Function to Delete Forms
@permission_required('ms.MSt_Admin_View')
def msthesisdelete(request, form_id):
    form = get_object_or_404(MSThesisPOS, pk=form_id)
    form.delete()
    return redirect('index')



#MS Coursework Function to Approve Forms for Advisors
@permission_required('ms.MSc_Advisor_View')
def mscourseadvisorapprove(request, form_id):
    # form = MSCoursePOS.objects.get(pk=form_id)
    form = get_object_or_404(MSCoursePOS, pk=form_id)
    if ((form.state == "DGSRejected") or (form.state == "Approved")):
        messages.add_message(request, messages.ERROR, "Advisors cannot approve forms already approved or rejected by the DGS.")
        return redirect('advisor-mscourse-detail', pk=form_id)

    form.state = "DGSPending"
    form.save()
    list = MSCoursePOS.objects.filter((~Q(pk=form_id))&Q(state="AdvisorPending"))
    if not list:
        return redirect('advisor-mscourse')
    else:
        return redirect('advisor-mscourse-detail', pk=list[0])


#Function to Add Comments to MS Coursework Forms for DGS and Reject Form
@permission_required('ms.MSc_Advisor_View')
def mscourseadvisorcomment(request, form_id):
    object = get_object_or_404(MSCoursePOS, pk=form_id)
    if ((object.state == "DGSRejected") | (object.state == "Approved")):
        messages.add_message(request, messages.ERROR, "Advisors cannot reject forms already approved or rejected by the DGS.")
        return redirect('advisor-mscourse-detail', pk=form_id)

    if request.method == "POST":
        form = MSCourseCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.form = object
            comment.authortype = "Advisor"
            comment.save()
            object.state = "AdvisorRejected"
            object.save()

            subject, from_email = 'POS Form Rejection', 'gradops@ece.duke.edu'
            plaintext = get_template('rejection.txt')
            htmly = get_template('rejection.html')

            recipient = object.owner.email
            first_name = object.owner.first_name
            logger.error("Recipient is:"+recipient)
            d = { 'first_name': first_name }

            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


            list = MSCoursePOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
            if not list:
                return redirect('advisor-mscourse')
            else:
                return redirect('advisor-mscourse-detail', pk=list[0])

    else:
        form = MSCourseCommentForm()
    return render(request, 'comment.html', {'form': form})



#MS Coursework Function to Approve Forms for DGS
@permission_required('ms.MSc_DGS_View')
def mscoursedgsapprove(request, form_id):
    # form = MSCoursePOS.objects.get(pk=form_id)
    form = get_object_or_404(MSCoursePOS, pk=form_id)
    if ((form.state == "AdvisorRejected") or (form.state == "AdvisorPending")):
        messages.add_message(request, messages.ERROR, "The DGS cannot approve forms that haven't been approved by an Advisor.")
        return redirect('dgs-mscourse-detail', pk=form_id)

    form.state = "Approved"
    form.save()
    subject, from_email = 'POS Form Approval', 'gradops@ece.duke.edu'
    plaintext = get_template('approval.txt')
    htmly = get_template('approval.html')

    first_name = form.owner.first_name
    d = { 'first_name': first_name }

    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    list = MSCoursePOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
    if not list:
        return redirect('dgs-mscourse')
    else:
        return redirect('dgs-mscourse-detail', pk=list[0])


#Function to Add Comments to MS Coursework Forms for DGS and Reject Form
@permission_required('ms.MSc_DGS_View')
def mscoursedgscomment(request, form_id):
    object = get_object_or_404(MSCoursePOS, pk=form_id)
    if ((object.state == "AdvisorRejected") | (object.state == "AdvisorPending")):
        messages.add_message(request, messages.ERROR, "The DGS cannot reject forms that haven't been rejected by an Advisor.")
        return redirect('dgs-mscourse-detail', pk=form_id)

    if request.method == "POST":
        form = MSCourseCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.form = object
            comment.authortype = "DGS"
            comment.save()
            object.state = "DGSRejected"
            object.save()


            subject, from_email = 'POS Form Rejection', 'gradops@ece.duke.edu'
            plaintext = get_template('rejection.txt')
            htmly = get_template('rejection.html')

            recipient = object.owner.email
            first_name = object.owner.first_name
            d = { 'first_name': first_name }

            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


            list = MSCoursePOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
            if not list:
                return redirect('dgs-mscourse')
            else:
                return redirect('dgs-mscourse-detail', pk=list[0])

    else:
        form = MSCourseCommentForm()
    return render(request, 'comment.html', {'form': form})


#Allows DGS to search for forms: HISTORY PAGE
@permission_required('ms.MSc_DGS_View')
def MSCoursePOSsearch(request):
    posfilter = MSCoursePOSFilter(request.GET, queryset=MSCoursePOS.objects.filter((Q(state="Approved")|Q(state="DGSRejected"))))
    pos_list = posfilter.qs
    type = "MSCoursePOS"
    usertype = "DGS"
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
         'users':users, 'type':type, 'page':page, 'search':'first',
         'usertype':usertype,}
    # return render(request, 'search.html', {'filter': posfilter})
    return render(request, 'search.html', args)


#MS PROJECT FUNCTIONS

#MS Project Function to Approve Forms for Advisors
@permission_required('ms.MSp_Advisor_View')
def msprojectadvisorapprove(request, form_id):
    # form = MSProjectPOS.objects.get(pk=form_id)
    form = get_object_or_404(MSProjectPOS, pk=form_id)
    if ((form.state == "DGSRejected") or (form.state == "Approved")):
        messages.add_message(request, messages.ERROR, "The DGS cannot approve forms that haven't been approved by an Advisor.")
        return redirect('advisor-msproject-detail', pk=form_id)

    form.state = "DGSPending"
    form.save()
    list = MSProjectPOS.objects.filter((~Q(pk=form_id))&Q(state="AdvisorPending"))
    if not list:
        return redirect('advisor-msproject')
    else:
        return redirect('advisor-msproject-detail', pk=list[0])


#Function to Add Comments to MS Project Forms for DGS and Reject Form
@permission_required('ms.MSp_Advisor_View')
def msprojectadvisorcomment(request, form_id):
    object = get_object_or_404(MSProjectPOS, pk=form_id)
    if ((object.state == "DGSRejected") | (object.state == "Approved")):
        messages.add_message(request, messages.ERROR, "Advisors cannot reject forms already approved or rejected by the DGS.")
        return redirect('advisor-msproject-detail', pk=form_id)

    if request.method == "POST":
        form = MSProjectCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.form = object
            comment.authortype = "Advisor"
            comment.save()
            object.state = "AdvisorRejected"
            object.save()

            subject, from_email = 'POS Form Rejection', 'gradops@ece.duke.edu'
            plaintext = get_template('rejection.txt')
            htmly = get_template('rejection.html')


            recipient = object.owner.email
            first_name = object.owner.first_name
            logger.error("Recipient is:"+recipient)
            d = { 'first_name': first_name }

            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


            list = MSProjectPOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
            if not list:
                return redirect('advisor-msproject')
            else:
                return redirect('advisor-msproject-detail', pk=list[0])

    else:
        form = MSProjectCommentForm()
    return render(request, 'comment.html', {'form': form})


#MS Project Function to Approve Forms for DGS
@permission_required('ms.MSp_DGS_View')
def msprojectdgsapprove(request, form_id):
    # form = MSProjectPOS.objects.get(pk=form_id)
    form = get_object_or_404(MSProjectPOS, pk=form_id)
    if ((form.state == "AdvisorRejected") or (form.state == "AdvisorPending")):
        messages.add_message(request, messages.ERROR, "The DGS cannot approve forms that haven't been approved by an Advisor.")
        return redirect('dgs-msproject-detail', pk=form_id)

    form.state = "Approved"
    form.save()
    subject, from_email = 'POS Form Approval', 'gradops@ece.duke.edu'
    plaintext = get_template('approval.txt')
    htmly = get_template('approval.html')

    first_name = form.owner.first_name
    d = { 'first_name': first_name }

    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    list = MSProjectPOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
    if not list:
        return redirect('dgs-msproject')
    else:
        return redirect('dgs-msproject-detail', pk=list[0])


#Function to Add Comments to MS Project Forms for DGS and Reject Form
@permission_required('ms.MSp_DGS_View')
def msprojectdgscomment(request, form_id):
    object = get_object_or_404(MSProjectPOS, pk=form_id)
    if ((object.state == "AdvisorRejected") | (object.state == "AdvisorPending")):
        messages.add_message(request, messages.ERROR, "The DGS cannot reject forms that haven't been rejected by an Advisor.")
        return redirect('dgs-msproject-detail', pk=form_id)

    if request.method == "POST":
        form = MSProjectCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.form = object
            comment.authortype = "DGS"
            comment.save()
            object.state = "DGSRejected"
            object.save()

            recipient = object.owner.email
            subject, from_email = 'POS Form Rejection', 'gradops@ece.duke.edu'
            plaintext = get_template('rejection.txt')
            htmly = get_template('rejection.html')

            first_name = object.owner.first_name
            d = { 'first_name': first_name }

            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()



            list = MSProjectPOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
            if not list:
                return redirect('dgs-msproject')
            else:
                return redirect('dgs-msproject-detail', pk=list[0])

    else:
        form = MSProjectCommentForm()
    return render(request, 'comment.html', {'form': form})

#Allows DGS to search for forms: HISTORY PAGE
@permission_required('ms.MSp_DGS_View')
def MSProjectPOSsearch(request):
    posfilter = MSProjectPOSFilter(request.GET, queryset=MSProjectPOS.objects.filter((Q(state="Approved")|Q(state="DGSRejected"))))
    pos_list = posfilter.qs
    type = "MSProjectPOS"
    usertype = "DGS"
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
         'users':users, 'type':type, 'page':page, 'search':'first',
         'usertype':usertype,}
    return render(request, 'search.html', args)



#MS Thesis Functions
#MS Thesis Function to Approve Forms for Advisors
@permission_required('ms.MSt_Advisor_View')
def msthesisadvisorapprove(request, form_id):
    # form = MSThesisPOS.objects.get(pk=form_id)
    form = get_object_or_404(MSThesisPOS, pk=form_id)
    if ((form.state == "DGSRejected") or (form.state == "Approved")):
        messages.add_message(request, messages.ERROR, "The DGS cannot approve forms that haven't been approved by an Advisor.")
        return redirect('advisor-msthesis-detail', pk=form_id)

    form.state = "DGSPending"
    form.save()
    list = MSThesisPOS.objects.filter((~Q(pk=form_id))&Q(state="AdvisorPending"))
    if not list:
        return redirect('advisor-msthesis')
    else:
        return redirect('advisor-msthesis-detail', pk=list[0])


#Function to Add Comments to MS Thesis Forms for DGS and Reject Form
@permission_required('ms.MSt_Advisor_View')
def msthesisadvisorcomment(request, form_id):
    object = get_object_or_404(MSThesisPOS, pk=form_id)
    if ((object.state == "DGSRejected") | (object.state == "Approved")):
        messages.add_message(request, messages.ERROR, "Advisors cannot reject forms already approved or rejected by the DGS.")
        return redirect('advisor-msthesis-detail', pk=form_id)

    if request.method == "POST":
        form = MSThesisCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.form = object
            comment.authortype = "Advisor"
            comment.save()
            object.state = "AdvisorRejected"
            object.save()

            subject, from_email = 'POS Form Rejection', 'gradops@ece.duke.edu'
            plaintext = get_template('rejection.txt')
            htmly = get_template('rejection.html')

            recipient = object.owner.email
            first_name = object.owner.first_name
            logger.error("Recipient is:"+recipient)
            d = { 'first_name': first_name }

            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


            list = MSThesisPOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
            if not list:
                return redirect('advisor-msthesis')
            else:
                return redirect('advisor-msthesis-detail', pk=list[0])

    else:
        form = MSThesisCommentForm()
    return render(request, 'comment.html', {'form': form})


#MS Thesis Function to Approve Forms for DGS
@permission_required('ms.MSt_DGS_View')
def msthesisdgsapprove(request, form_id):
    # form = MSThesisPOS.objects.get(pk=form_id)
    form = get_object_or_404(MSThesisPOS, pk=form_id)
    if ((form.state == "AdvisorRejected") or (form.state == "AdvisorPending")):
        messages.add_message(request, messages.ERROR, "The DGS cannot approve forms that haven't been approved by an Advisor.")
        return redirect('dgs-msthesis-detail', pk=form_id)

    form.state = "Approved"
    form.save()
    subject, from_email = 'POS Form Approval', 'gradops@ece.duke.edu'
    plaintext = get_template('approval.txt')
    htmly = get_template('approval.html')

    first_name = form.owner.first_name
    d = { 'first_name': first_name }

    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    list = MSThesisPOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
    if not list:
        return redirect('dgs-msthesis')
    else:
        return redirect('dgs-msthesis-detail', pk=list[0])


#Function to Add Comments to MS Thesis Forms for DGS and Reject Form
@permission_required('ms.MSt_DGS_View')
def msthesisdgscomment(request, form_id):
    object = get_object_or_404(MSThesisPOS, pk=form_id)
    if ((object.state == "AdvisorRejected") | (object.state == "AdvisorPending")):
        messages.add_message(request, messages.ERROR, "The DGS cannot reject forms that haven't been rejected by an Advisor.")
        return redirect('dgs-msthesis-detail', pk=form_id)

    if request.method == "POST":
        form = MSThesisCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.form = object
            comment.authortype = "DGS"
            comment.save()
            object.state = "DGSRejected"
            object.save()

            subject, from_email = 'POS Form Rejection', 'gradops@ece.duke.edu'
            plaintext = get_template('rejection.txt')
            htmly = get_template('rejection.html')

            recipient = object.owner.email
            first_name = object.owner.first_name
            d = { 'first_name': first_name }

            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()



            list = MSThesisPOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
            if not list:
                return redirect('dgs-msthesis')
            else:
                return redirect('dgs-msthesis-detail', pk=list[0])

    else:
        form = MSThesisCommentForm()
    return render(request, 'comment.html', {'form': form})


#Allows DGS to search for forms: HISTORY PAGE
@permission_required('ms.MSt_DGS_View')
def MSThesisPOSsearch(request):
    posfilter = MSThesisPOSFilter(request.GET, queryset=MSThesisPOS.objects.filter((Q(state="Approved")|Q(state="DGSRejected"))))
    pos_list = posfilter.qs
    type = "MSThesisPOS"
    usertype = "DGS"
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
         'users':users, 'type':type, 'page':page, 'search':'first',
         'usertype':usertype,}
    # return render(request, 'search.html', {'filter': posfilter})
    return render(request, 'search.html', args)



#MS Form Option Views
@permission_required('ms.MSc_Advisor_View')
@permission_required('ms.MSp_Advisor_View')
@permission_required('ms.MSt_Advisor_View')
def msadvisoroption(request):
    """
    View function for advisor to pick between viewing 1 of 3 MS Forms
    """
    usertype = "Advisor"
    args = {'usertype':usertype,}

    return render(
        request,
        'MSoption.html',
        args
    )

@permission_required('ms.MSc_DGS_View')
@permission_required('ms.MSp_DGS_View')
@permission_required('ms.MSt_DGS_View')
def msdgsoption(request):
    """
    View function for DGS to pick between viewing 1 of 3 MS Forms
    """
    usertype = "DGS"
    args = {'usertype':usertype,}

    return render(
        request,
        'MSoption.html',
        args
    )

@permission_required('ms.MSc_Student_View')
@permission_required('ms.MSp_Student_View')
@permission_required('ms.MSt_Student_View')
def msstudentoption(request):
    """
    View function for student to pick between viewing 1 of 3 MS Forms
    """
    usertype = "MS"
    args = {'usertype':usertype,}

    return render(
        request,
        'MSoption.html',
        args
    )

@permission_required('ms.MSc_Student_Create')
@permission_required('ms.MSp_Student_Create')
@permission_required('ms.MSt_Student_Create')
def msstudentoptioncreate(request):
    """
    View function for advisor to pick between creating 1 of 3 MS Forms
    """
    return render(
        request,
        'MSstudentoptioncreate.html',
    )
