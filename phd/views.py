from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.forms.utils import ErrorList
from phd.models import *
from phd.forms import *
from shared.models import *
from django.contrib.auth.decorators import permission_required
from search_listview.list import SearchableListView
from phd.filters import *
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, send_mail
from django.utils.html import strip_tags
from django.template.loader import get_template, render_to_string
from django.template import Context
# Create your views here.

class PHDBSListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'phd.PHDBS_Student_View'
    model = PHDBachelorPOS
    context_object_name = 'form_list'
    template_name = 'list.html'
    paginate_by = 10

    def get_queryset(self):
        return PHDBachelorPOS.objects.filter(owner=self.request.user)

    def get_approved(self):
        return PHDBachelorPOS.objects.filter(Q(owner=self.request.user)&Q(state="Approved"))

    def get_rejected(self):
        return PHDBachelorPOS.objects.filter(Q(owner=self.request.user)&(Q(state="AdvisorRejected")|Q(state="DGSRejected")))

    def get_pending(self):
        return PHDBachelorPOS.objects.filter(Q(owner=self.request.user)&(Q(state="AdvisorPending")|Q(state="DGSPending")))

    def get_context_data(self, **kwargs):
        context = super(PHDBSListView, self).get_context_data(**kwargs)
        context['approvedcount'] = self.get_approved().count()
        context['rejectedcount'] = self.get_rejected().count()
        context['pendingcount'] = self.get_pending().count()
        context['list'] = "PHDB"
        context['usertype'] = "PhD"
        return context


class PHDBSDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'phd.PHDBS_Student_View'
    model = PHDBachelorPOS
    template_name = 'PHDBS_detail.html'

    def get_object(self):
        """Returns the MEngPOS instance that the view displays"""
        owner = PHDBachelorPOS.objects.filter(owner=self.request.user)
        object = PHDBachelorPOS.objects.get(pk=self.kwargs.get("pk"))
        if (object.owner == self.request.user):
            return object
        else:
            raise PermissionDenied


    def get_context_data(self, **kwargs):
        context = super(PHDBSDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "PhD"
        return context


class PHDBSUpdateView(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    permission_required = 'phd.PHDBS_Student_View'
    model = PHDBachelorPOS
    form_class = PHDBSPOSForm
    template_name_suffix = '_phdbs_form'

    def get_object(self):
        """Returns the PHDBachelorPOS instance that the view displays"""
        owner = PHDBachelorPOS.objects.filter(owner=self.request.user)
        object = PHDBachelorPOS.objects.get(pk=self.kwargs.get("pk"))
        if (object.owner == self.request.user):
            return object
        else:
            raise PermissionDenied

    def dispatch(self, request, *args, **kwargs):
        object = PHDBachelorPOS.objects.get(pk=self.kwargs.get("pk"))
        if ((object.state == "AdvisorPending") or (object.state == "DGSPending") or (object.state == "Approved")):
            messages.add_message(self.request, messages.ERROR, "Students can only update forms when they are " \
            "rejected.")
            return redirect('phdbachelor-detail', pk=self.kwargs.get("pk"))

        else:
            return super(PHDBSUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        x =  PHDBachelorPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        y =  PHDMasterPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        if (len(x) + len(y) > 0):
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
            u'Students may only resubmit a form if they do not have a current form under review.'
            ])
            return self.form_invalid(form)

        user = self.request.user
        form.instance.owner = user
        form.instance.state = "AdvisorPending"
        return super(PHDBSUpdateView, self).form_valid(form)


class PHDBSAdvisorListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'phd.PHDBS_Advisor_View'
    model = PHDBachelorPOS
    context_object_name = 'form_list'
    template_name = 'list.html'
    paginate_by = 10

    def get_queryset(self):
        return PHDBachelorPOS.objects.filter(Q(owner__advisor=self.request.user)&Q(state="AdvisorPending"))

    def get_context_data(self, **kwargs):
        context = super(PHDBSAdvisorListView, self).get_context_data(**kwargs)
        context['advisorcount'] = self.get_queryset().count()
        context['list'] = "PHDB"
        context['usertype'] = "Advisor"
        return context

class PHDBSAdvisorDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'phd.PHDBS_Advisor_View'
    model = PHDBachelorPOS
    template_name = 'PHDBS_detail.html'

    def get_object(self):
        """Returns the PHDBachelorPOS instance that the view displays"""
        object = PHDBachelorPOS.objects.get(pk=self.kwargs.get("pk"))
        ##Restrict Advisor View --> Unable to see old form if DGSRejected or Approved
        if ((object.state == "DGSRejected") or (object.state == "Approved")):
            raise PermissionDenied
        if (object.owner.advisor == self.request.user):
            return object
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(PHDBSAdvisorDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "Advisor"
        return context

class PHDBSAdvisorHistoryView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'phd.PHDBS_Advisor_View'
    model = PHDBachelorPOS
    context_object_name = 'form_list'
    template_name = 'history.html'
    paginate_by = 10

    def get_queryset(self):
        return PHDBachelorPOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="AdvisorRejected")|Q(state="DGSPending")))

    def get_approved(self):
        return PHDBachelorPOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="DGSPending")))

    def get_rejected(self):
        return PHDBachelorPOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="AdvisorRejected")))

    def get_context_data(self, **kwargs):
        context = super(PHDBSAdvisorHistoryView, self).get_context_data(**kwargs)
        context['advisorapproved'] = self.get_approved().count()
        context['advisorrejected'] = self.get_rejected().count()
        context['history'] = "PHDB"
        return context


class PHDBSDGSListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'phd.PHDBS_DGS_View'
    model = PHDBachelorPOS
    context_object_name = 'form_list'
    template_name = 'dgslist.html'
    paginate_by = 10

    def get_queryset(self):
        return PHDBachelorPOS.objects.filter(Q(state="DGSPending"))

    def get_context_data(self, **kwargs):
        context = super(PHDBSDGSListView, self).get_context_data(**kwargs)
        context['dgscount'] = self.get_queryset().count()
        context['list'] = "PHDB"
        return context


class PHDBSDGSDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'phd.PHDBS_DGS_View'
    model = PHDBachelorPOS
    template_name = 'PHDBS_detail.html'


    def get_context_data(self, **kwargs):
        context = super(PHDBSDGSDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "DGS"
        return context

class PHDBSDGSHistoryView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'phd.PHDBS_DGS_View'
    model = PHDBachelorPOS
    context_object_name = 'form_list'
    template_name = 'history.html'
    paginate_by = 10

    def get_queryset(self):
        return PHDBachelorPOS.objects.filter(Q(state="Approved")|Q(state="DGSRejected"))

    def get_rejected(self):
        return PHDBachelorPOS.objects.filter(Q(state="DGSRejected"))

    def get_approved(self):
        return PHDBachelorPOS.objects.filter(Q(state="Approved"))

    def get_context_data(self, **kwargs):
        context = super(PHDBSDGSHistoryView, self).get_context_data(**kwargs)
        context['dgsrejected'] = self.get_rejected().count()
        context['dgsapproved'] = self.get_approved().count()
        context['history'] = "PHDB"
        return context

class AdminPHDBSDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'phd.PHDBS_Admin_View'
    model = PHDBachelorPOS
    template_name = 'PHDBS_detail.html'


    def get_context_data(self, **kwargs):
        context = super(AdminPHDBSDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "Administrator"
        return context

class PHDMSListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'phd.PHDMS_Student_View'
    model = PHDMasterPOS
    context_object_name = 'form_list'
    template_name = 'list.html'
    paginate_by = 10

    def get_queryset(self):
        return PHDMasterPOS.objects.filter(owner=self.request.user)

    def get_approved(self):
        return PHDMasterPOS.objects.filter(Q(owner=self.request.user)&Q(state="Approved"))

    def get_rejected(self):
        return PHDMasterPOS.objects.filter(Q(owner=self.request.user)&(Q(state="AdvisorRejected")|Q(state="DGSRejected")))

    def get_pending(self):
        return PHDMasterPOS.objects.filter(Q(owner=self.request.user)&(Q(state="AdvisorPending")|Q(state="DGSPending")))

    def get_context_data(self, **kwargs):
        context = super(PHDMSListView, self).get_context_data(**kwargs)
        context['approvedcount'] = self.get_approved().count()
        context['rejectedcount'] = self.get_rejected().count()
        context['pendingcount'] = self.get_pending().count()
        context['list'] = "PHDM"
        context['usertype'] = "PhD"
        return context


class PHDMSDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'phd.PHDMS_Student_View'
    model = PHDMasterPOS
    template_name = 'PHDMS_detail.html'


    def get_object(self):
        """Returns the MEngPOS instance that the view displays"""
        owner = PHDMasterPOS.objects.filter(owner=self.request.user)
        object = PHDMasterPOS.objects.get(pk=self.kwargs.get("pk"))
        if (object.owner == self.request.user):
            return object
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(PHDMSDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "PhD"
        return context

class PHDMSUpdateView(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    permission_required = 'phd.PHDMS_Student_View'
    model = PHDMasterPOS
    form_class = PHDMSPOSForm
    template_name_suffix = '_phdms_form'

    def get_object(self):
        """Returns the PHDBachelorPOS instance that the view displays"""
        owner = PHDMasterPOS.objects.filter(owner=self.request.user)
        object = PHDMasterPOS.objects.get(pk=self.kwargs.get("pk"))
        if (object.owner == self.request.user):
            return object
        else:
            raise PermissionDenied

    def dispatch(self, request, *args, **kwargs):
        object = PHDMasterPOS.objects.get(pk=self.kwargs.get("pk"))
        if ((object.state == "AdvisorPending") or (object.state == "DGSPending") or (object.state == "Approved")):
            messages.add_message(self.request, messages.ERROR, "Students can only update forms when they are " \
            "rejected.")
            return redirect('phdmaster-detail', pk=self.kwargs.get("pk"))

        else:
            return super(PHDMSUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        x =  PHDBachelorPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        y =  PHDMasterPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        if (len(x) + len(y) > 0):
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
            u'Students may only resubmit a form if they do not have a current form under review.'
            ])
            return self.form_invalid(form)

        user = self.request.user
        form.instance.owner = user
        form.instance.state = "AdvisorPending"
        return super(PHDMSUpdateView, self).form_valid(form)


class PHDMSAdvisorListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'phd.PHDMS_Advisor_View'
    model = PHDMasterPOS
    context_object_name = 'form_list'
    template_name = 'list.html'
    paginate_by = 10

    def get_queryset(self):
        return PHDMasterPOS.objects.filter(Q(owner__advisor=self.request.user)&Q(state="AdvisorPending"))

    def get_context_data(self, **kwargs):
        context = super(PHDMSAdvisorListView, self).get_context_data(**kwargs)
        context['advisorcount'] = self.get_queryset().count()
        context['list'] = "PHDM"
        context['usertype'] = "Advisor"
        return context

class PHDMSAdvisorDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'phd.PHDMS_Advisor_View'
    model = PHDMasterPOS
    template_name = 'PHDMS_detail.html'

    def get_object(self):
        """Returns the PHDMasterPOS instance that the view displays"""
        object = PHDMasterPOS.objects.get(pk=self.kwargs.get("pk"))
        ##Restrict Advisor View --> Unable to see old form if DGSRejected or Approved
        if ((object.state == "DGSRejected") or (object.state == "Approved")):
            raise PermissionDenied
        if (object.owner.advisor == self.request.user):
            return object
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(PHDMSAdvisorDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "Advisor"
        return context

class PHDMSAdvisorHistoryView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'phd.PHDMS_Advisor_View'
    model = PHDMasterPOS
    context_object_name = 'form_list'
    template_name = 'history.html'
    paginate_by = 10

    def get_queryset(self):
        return PHDMasterPOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="AdvisorRejected")|Q(state="DGSPending")))

    def get_approved(self):
        return PHDMasterPOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="DGSPending")))

    def get_rejected(self):
        return PHDMasterPOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="AdvisorRejected")))

    def get_context_data(self, **kwargs):
        context = super(PHDMSAdvisorHistoryView, self).get_context_data(**kwargs)
        context['advisorapproved'] = self.get_approved().count()
        context['advisorrejected'] = self.get_rejected().count()
        context['history'] = "PHDM"
        return context


class PHDMSDGSListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'phd.PHDMS_DGS_View'
    model = PHDMasterPOS
    context_object_name = 'form_list'
    template_name = 'dgslist.html'


    def get_queryset(self):
        return PHDMasterPOS.objects.filter(Q(state="DGSPending"))

    def get_context_data(self, **kwargs):
        context = super(PHDMSDGSListView, self).get_context_data(**kwargs)
        context['dgscount'] = self.get_queryset().count()
        context['list'] = "PHDM"
        return context

class PHDMSDGSDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'phd.PHDMS_DGS_View'
    model = PHDMasterPOS
    template_name = 'PHDMS_detail.html'


    def get_context_data(self, **kwargs):
        context = super(PHDMSDGSDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "DGS"
        return context

class PHDMSDGSHistoryView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'phd.PHDMS_DGS_View'
    model = PHDMasterPOS
    context_object_name = 'form_list'
    template_name = 'history.html'
    paginate_by = 10

    def get_queryset(self):
        return PHDMasterPOS.objects.filter(Q(state="Approved")|Q(state="DGSRejected"))

    def get_rejected(self):
        return PHDMasterPOS.objects.filter(Q(state="DGSRejected"))

    def get_approved(self):
        return PHDMasterPOS.objects.filter(Q(state="Approved"))

    def get_context_data(self, **kwargs):
        context = super(PHDMSDGSHistoryView, self).get_context_data(**kwargs)
        context['dgsrejected'] = self.get_rejected().count()
        context['dgsapproved'] = self.get_approved().count()
        context['history'] = "PHDM"
        return context

class AdminPHDMSDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'phd.PHDMS_Admin_View'
    model = PHDMasterPOS
    template_name = 'PHDMS_detail.html'


    def get_context_data(self, **kwargs):
        context = super(AdminPHDMSDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "Administrator"
        return context

class PHDBSPOSCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'phd.PHDBS_Student_Create'
    model = PHDBachelorPOS
    form_class = PHDBSPOSForm
    template_name_suffix = '_phdbs_form'

    def form_valid(self, form):
        # Sets the owner as the person who created the form
        x =  PHDBachelorPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        y =  PHDMasterPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        if (len(x) + len(y) > 0):
            # raise ValidationError("Students may only submit a new form if they do not have a current form under review.")
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
            u'Students may only submit a new form if they do not have a current form under review.'
            ])
            return self.form_invalid(form)

        user = self.request.user
        form.instance.owner = user
        form.instance.state = "AdvisorPending"
        return super(PHDBSPOSCreate, self).form_valid(form)

class PHDMSPOSCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'phd.PHDMS_Student_Create'
    model = PHDMasterPOS
    form_class = PHDMSPOSForm
    template_name_suffix = '_phdms_form'

    def form_valid(self, form):
        # Sets the owner as the person who created the form
        x =  PHDBachelorPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        y =  PHDMasterPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        if (len(x) + len(y) > 0):
            # raise ValidationError("Students may only submit a new form if they do not have a current form under review.")
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
            u'Students may only submit a new form if they do not have a current form under review.'
            ])
            return self.form_invalid(form)

        user = self.request.user
        form.instance.owner = user
        form.instance.state = "AdvisorPending"
        return super(PHDMSPOSCreate, self).form_valid(form)


class AdminPHDBSPOSCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'phd.PHDBS_Admin_Create'
    model = PHDBachelorPOS
    form_class = AdminPHDBSPOSForm
    template_name_suffix = '_phdbs_form'
    def form_valid(self, form):
        form.instance.state = "AdvisorPending"
        return super(AdminPHDBSPOSCreate, self).form_valid(form)

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
        context = super(AdminPHDBSPOSCreate, self).get_context_data(**kwargs)
        context['usertype'] = "Administrator"
        return context


class AdminPHDMSPOSCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'phd.PHDMS_Admin_Create'
    model = PHDMasterPOS
    form_class = AdminPHDMSPOSForm
    template_name_suffix = '_phdms_form'
    def form_valid(self, form):
        form.instance.state = "AdvisorPending"
        return super(AdminPHDMSPOSCreate, self).form_valid(form)

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
        context = super(AdminPHDMSPOSCreate, self).get_context_data(**kwargs)
        context['usertype'] = "Administrator"
        return context


#Allows Admin to search for forms: HISTORY PAGE
@permission_required('phd.PHDBS_Admin_View')
def AdminPHDBSPOSsearch(request):
    posfilter = PHDBachelorPOSFilter(request.GET, queryset=PHDBachelorPOS.objects.all())
    pos_list = posfilter.qs
    type = "PHDBachelorPOS"
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
@permission_required('phd.PHDMS_Admin_View')
def AdminPHDMSPOSsearch(request):
    posfilter = PHDMasterPOSFilter(request.GET, queryset=PHDMasterPOS.objects.all())
    pos_list = posfilter.qs
    type = "PHDMasterPOS"
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
    return render(request, 'search.html', args)

#PhD Bachelor Function to Delete Forms
@permission_required('phd.PHDBS_Admin_View')
def phdbsdelete(request, form_id):
    form = get_object_or_404(PHDBachelorPOS, pk=form_id)
    form.delete()
    return redirect('index')

#Phd Master Function to Delete Forms
@permission_required('phd.PHDMS_Admin_View')
def phdmsdelete(request, form_id):
    form = get_object_or_404(PHDMasterPOS, pk=form_id)
    form.delete()
    return redirect('index')


#PHD BS Function to Approve Forms for Advisors
@permission_required('phd.PHDBS_Advisor_View')
def phdbacheloradvisorapprove(request, form_id):
    form = get_object_or_404(PHDBachelorPOS, pk=form_id)
    if ((form.state == "DGSRejected") or (form.state == "Approved")):
        messages.add_message(request, messages.ERROR, "Advisors cannot approve forms already approved or rejected by the DGS.")
        return redirect('advisor-phdbachelor-detail', pk=form_id)

    form.state = "DGSPending"
    form.save()
    list = PHDBachelorPOS.objects.filter((~Q(pk=form_id))&Q(state="AdvisorPending"))
    if not list:
        return redirect('advisor-phdbachelor')
    else:
        return redirect('advisor-phdbachelor-detail', pk=list[0])


#Function to Add Comments to PHD Bachelor Forms for DGS and Reject Form
@permission_required('phd.PHDBS_Advisor_View')
def phdbacheloradvisorcomment(request, form_id):
    object = get_object_or_404(PHDBachelorPOS, pk=form_id)
    if ((object.state == "DGSRejected") | (object.state == "Approved")):
        messages.add_message(request, messages.ERROR, "Advisors cannot reject forms already approved or rejected by the DGS.")
        return redirect('advisor-phdbachelor-detail', pk=form_id)

    if request.method == "POST":
        form = PHDBachelorCommentForm(request.POST)
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
            d = { 'first_name': first_name }

            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


            list = PHDBachelorPOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
            if not list:
                return redirect('advisor-phdbachelor')
            else:
                return redirect('advisor-phdbachelor-detail', pk=list[0])

    else:
        form = PHDBachelorCommentForm()
    return render(request, 'comment.html', {'form': form})


#PHD Bachelor Function to Approve Forms for DGS
@permission_required('phd.PHDBS_DGS_View')
def phdbachelordgsapprove(request, form_id):
    form = get_object_or_404(PHDBachelorPOS, pk=form_id)
    if ((form.state == "AdvisorRejected") or (form.state == "AdvisorPending")):
        messages.add_message(request, messages.ERROR, "The DGS cannot approve forms that haven't been approved by an Advisor.")
        return redirect('dgs-phdbachelor-detail', pk=form_id)

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
    list = PHDBachelorPOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
    if not list:
        return redirect('dgs-phdbachelor')
    else:
        return redirect('dgs-phdbachelor-detail', pk=list[0])


#Function to Add Comments to PHD Bachelor Forms for DGS and Reject Form
@permission_required('phd.PHDBS_DGS_View')
def phdbachelordgscomment(request, form_id):
    object = get_object_or_404(PHDBachelorPOS, pk=form_id)
    if ((object.state == "AdvisorRejected") | (object.state == "AdvisorPending")):
        messages.add_message(request, messages.ERROR, "The DGS cannot reject forms that haven't been rejected by an Advisor.")
        return redirect('dgs-phdbachelor-detail', pk=form_id)

    if request.method == "POST":
        form = PHDBachelorCommentForm(request.POST)
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



            list = PHDBachelorPOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
            if not list:
                return redirect('dgs-phdbachelor')
            else:
                return redirect('dgs-phdbachelor-detail', pk=list[0])

    else:
        form = PHDBachelorCommentForm()
    return render(request, 'comment.html', {'form': form})


#PHD Master Function to Approve Forms for Advisors
@permission_required('phd.PHDMS_Advisor_View')
def phdmasteradvisorapprove(request, form_id):
    # form = MEngPOS.objects.get(pk=form_id)
    form = get_object_or_404(PHDMasterPOS, pk=form_id)
    if ((form.state == "DGSRejected") or (form.state == "Approved")):
        messages.add_message(request, messages.ERROR, "Advisors cannot approve forms already approved or rejected by the DGS.")
        return redirect('advisor-phdmaster-detail', pk=form_id)

    form.state = "DGSPending"
    form.save()
    list = PHDMasterPOS.objects.filter((~Q(pk=form_id))&Q(state="AdvisorPending"))
    if not list:
        return redirect('advisor-phdmaster')
    else:
        return redirect('advisor-phdmaster-detail', pk=list[0])


#Function to Add Comments to MS Project Forms for DGS and Reject Form
@permission_required('phd.PHDMS_Advisor_View')
def phdmasteradvisorcomment(request, form_id):
    object = get_object_or_404(PHDMasterPOS, pk=form_id)
    if ((object.state == "DGSRejected") | (object.state == "Approved")):
        messages.add_message(request, messages.ERROR, "Advisors cannot reject forms already approved or rejected by the DGS.")
        return redirect('advisor-phdmaster-detail', pk=form_id)

    if request.method == "POST":
        form = PHDMasterCommentForm(request.POST)
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
            d = { 'first_name': first_name }

            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


            list = PHDMasterPOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
            if not list:
                return redirect('advisor-phdmaster')
            else:
                return redirect('advisor-phdmaster-detail', pk=list[0])

    else:
        form = PHDMasterCommentForm()
    return render(request, 'comment.html', {'form': form})


#MS Project Function to Approve Forms for DGS
@permission_required('phd.PHDMS_DGS_View')
def phdmasterdgsapprove(request, form_id):
    # form = MEngPOS.objects.get(pk=form_id)
    form = get_object_or_404(PHDMasterPOS, pk=form_id)
    if ((form.state == "AdvisorRejected") or (form.state == "AdvisorPending")):
        messages.add_message(request, messages.ERROR, "The DGS cannot approve forms that haven't been approved by an Advisor.")
        return redirect('dgs-phdmaster-detail', pk=form_id)

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
    list = PHDMasterPOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
    if not list:
        return redirect('dgs-phdmaster')
    else:
        return redirect('dgs-phdmaster-detail', pk=list[0])


#Function to Add Comments to MS Project Forms for DGS and Reject Form
@permission_required('phd.PHDMS_DGS_View')
def phdmasterdgscomment(request, form_id):
    object = get_object_or_404(PHDMasterPOS, pk=form_id)
    if ((object.state == "AdvisorRejected") | (object.state == "AdvisorPending")):
        messages.add_message(request, messages.ERROR, "The DGS cannot reject forms that haven't been rejected by an Advisor.")
        return redirect('dgs-phdmaster-detail', pk=form_id)

    if request.method == "POST":
        form = PHDMasterCommentForm(request.POST)
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


            list = PHDMasterPOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
            if not list:
                return redirect('dgs-phdmaster')
            else:
                return redirect('dgs-phdmaster-detail', pk=list[0])

    else:
        form = PHDMasterCommentForm()
    return render(request, 'comment.html', {'form': form})

#Allows DGS to search for forms: HISTORY PAGE
@permission_required('phd.PHDBS_DGS_View')
def PHDBachelorPOSsearch(request):
    posfilter = PHDBachelorPOSFilter(request.GET, queryset=PHDBachelorPOS.objects.filter((Q(state="Approved")|Q(state="DGSRejected"))))
    pos_list = posfilter.qs
    type = "PHDBachelorPOS"
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

#Allows DGS to search for forms: HISTORY PAGE
@permission_required('phd.PHDMS_DGS_View')
def PHDMasterPOSsearch(request):
    posfilter = PHDMasterPOSFilter(request.GET, queryset=PHDMasterPOS.objects.filter((Q(state="Approved")|Q(state="DGSRejected"))))
    pos_list = posfilter.qs
    type = "PHDMasterPOS"
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


#PHD BS Form Option Views
@permission_required('phd.PHDBS_Advisor_View')
@permission_required('phd.PHDMS_Advisor_View')
def phdadvisoroption(request):
    """
    View function for advisor to pick between viewing 1 of 2 PHD Forms
    """
    usertype = "Advisor"
    args = {'usertype':usertype,}

    return render(
        request,
        'PHDoption.html',
        args
    )

@permission_required('phd.PHDBS_DGS_View')
@permission_required('phd.PHDMS_DGS_View')
def phddgsoption(request):
    """
    View function for DGS to pick between viewing 1 of 2 PHD Forms
    """
    usertype = "DGS"
    args = {'usertype':usertype,}

    return render(
        request,
        'PHDoption.html',
        args
    )

@permission_required('phd.PHDBS_Student_View')
@permission_required('phd.PHDMS_Student_View')
def phdstudentoption(request):
    """
    View function for student to pick between viewing 1 of 2 PHD Forms
    """
    usertype = "PhD"
    args = {'usertype':usertype,}

    return render(
        request,
        'PHDoption.html',
        args
    )

@permission_required('phd.PHDBS_Student_Create')
@permission_required('phd.PHDMS_Student_Create')
def phdstudentoptioncreate(request):
    """
    View function for student to pick between creating 1 of 2 PHD Forms
    """
    return render(
        request,
        'PHDstudentoptioncreate.html',
    )
