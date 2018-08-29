from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms.utils import ErrorList
from shared.models import *
from meng.models import *
from meng.forms import *
from django import forms
from django.contrib.auth.decorators import permission_required
from meng.filters import *
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.urls import reverse_lazy
from shared.urls import *
from django.core.mail import EmailMultiAlternatives, send_mail
from django.utils.html import strip_tags
from django.template.loader import get_template, render_to_string
from django.template import Context

logger = logging.getLogger('meng/views.py')


# Create your views here.
class MengListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'meng.MEng_Student_View'
    model = MEngPOS
    context_object_name = 'form_list'
    template_name = 'list.html'
    paginate_by = 10

    def get_queryset(self):
        return MEngPOS.objects.filter(owner=self.request.user)

    def get_approved(self):
        return MEngPOS.objects.filter(Q(owner=self.request.user)&Q(state="Approved"))

    def get_rejected(self):
        return MEngPOS.objects.filter(Q(owner=self.request.user)&(Q(state="AdvisorRejected")|Q(state="DGSRejected")))

    def get_pending(self):
        return MEngPOS.objects.filter(Q(owner=self.request.user)&(Q(state="AdvisorPending")|Q(state="DGSPending")))

    def get_context_data(self, **kwargs):
        context = super(MengListView, self).get_context_data(**kwargs)
        context['approvedcount'] = self.get_approved().count()
        context['rejectedcount'] = self.get_rejected().count()
        context['pendingcount'] = self.get_pending().count()
        context['list'] = "MEng"
        context['usertype'] = "MEng"
        return context


class MengDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'meng.MEng_Student_View'
    model = MEngPOS
    template_name = 'MEng_detail.html'


    def get_object(self):
        """Returns the MEngPOS instance that the view displays"""
        owner = MEngPOS.objects.filter(owner=self.request.user)
        object = MEngPOS.objects.get(pk=self.kwargs.get("pk"))
        if (object.owner == self.request.user):
            return object
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(MengDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "MEng"
        return context



class MengUpdateView(PermissionRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    permission_required = 'meng.MEng_Student_View'
    model = MEngPOS
    form_class = MEngPOSForm
    template_name_suffix = '_meng_form'

    def get_object(self):
        """Returns the MEngPOS instance that the view displays"""
        owner = MEngPOS.objects.filter(owner=self.request.user)
        object = MEngPOS.objects.get(pk=self.kwargs.get("pk"))
        if (object.owner == self.request.user):
            return object
        else:
            raise PermissionDenied

    def dispatch(self, request, *args, **kwargs):
        object = MEngPOS.objects.get(pk=self.kwargs.get("pk"))
        if ((object.state == "AdvisorPending") or (object.state == "DGSPending") or (object.state == "Approved")):
            messages.add_message(self.request, messages.ERROR, "Students can only update forms when they are " \
            "rejected.")
            return redirect('meng-detail', pk=self.kwargs.get("pk"))

        else:
            return super(MengUpdateView, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        x =  MEngPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        if (len(x) > 0):
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
            u'Students may only resubmit a form if they do not have a current form under review.'
            ])
            return self.form_invalid(form)

        user = self.request.user
        form.instance.owner = user
        form.instance.state = "AdvisorPending"
        return super(MengUpdateView, self).form_valid(form)


class MengAdvisorListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'meng.MEng_Advisor_View'
    model = MEngPOS
    context_object_name = 'form_list'
    template_name = 'list.html'
    paginate_by = 10

    def get_queryset(self):
        return MEngPOS.objects.filter(Q(owner__advisor=self.request.user)&Q(state="AdvisorPending"))

    def get_context_data(self, **kwargs):
        context = super(MengAdvisorListView, self).get_context_data(**kwargs)
        context['advisorcount'] = self.get_queryset().count()
        context['list'] = "MEng"
        context['usertype'] = "Advisor"
        return context

class MengAdvisorDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'meng.MEng_Advisor_View'
    model = MEngPOS
    template_name = 'MEng_detail.html'


    def get_object(self):
        """Returns the MEngPOS instance that the view displays"""
        object = MEngPOS.objects.get(pk=self.kwargs.get("pk"))
        ##Restrict Advisor View --> Unable to see old form if DGSRejected or Approved
        if ((object.state == "DGSRejected") or (object.state == "Approved")):
            raise PermissionDenied

        if (object.owner.advisor == self.request.user):
            return object
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(MengAdvisorDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "Advisor"
        return context


class MengAdvisorHistoryView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'meng.MEng_Advisor_View'
    model = MEngPOS
    context_object_name = 'form_list'
    template_name = 'history.html'
    paginate_by = 10

    def get_queryset(self):
        return MEngPOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="AdvisorRejected")|Q(state="DGSPending")))

    def get_approved(self):
        return MEngPOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="DGSPending")))

    def get_rejected(self):
        return MEngPOS.objects.filter(Q(owner__advisor=self.request.user)&(Q(state="AdvisorRejected")))

    def get_context_data(self, **kwargs):
        context = super(MengAdvisorHistoryView, self).get_context_data(**kwargs)
        context['advisorapproved'] = self.get_approved().count()
        context['advisorrejected'] = self.get_rejected().count()
        context['history'] = "MEng"
        return context


class MengDGSListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'meng.MEng_DGS_View'
    model = MEngPOS
    context_object_name = 'form_list'
    template_name = 'dgslist.html'
    paginate_by = 10

    def get_queryset(self):
        return MEngPOS.objects.filter(Q(state="DGSPending"))

    def get_context_data(self, **kwargs):
        context = super(MengDGSListView, self).get_context_data(**kwargs)
        context['dgscount'] = self.get_queryset().count()
        context['list'] = "MEng"
        return context

class MengDGSDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'meng.MEng_DGS_View'
    model = MEngPOS
    template_name = 'MEng_detail.html'


    def get_context_data(self, **kwargs):
        context = super(MengDGSDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "DGS"
        return context


class MengDGSHistoryView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'meng.MEng_DGS_View'
    model = MEngPOS
    context_object_name = 'form_list'
    template_name = 'history.html'
    paginate_by = 10

    def get_queryset(self):
        return MEngPOS.objects.filter(Q(state="Approved")|Q(state="DGSRejected"))

    def get_rejected(self):
        return MEngPOS.objects.filter(Q(state="DGSRejected"))

    def get_approved(self):
        return MEngPOS.objects.filter(Q(state="Approved"))

    def get_context_data(self, **kwargs):
        context = super(MengDGSHistoryView, self).get_context_data(**kwargs)
        context['dgsrejected'] = self.get_rejected().count()
        context['dgsapproved'] = self.get_approved().count()
        context['history'] = "MEng"
        return context


class AdminMengDetailView(PermissionRequiredMixin, LoginRequiredMixin, generic.DetailView):
    permission_required = 'meng.MEng_Admin_View'
    model = MEngPOS
    template_name = 'MEng_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AdminMengDetailView, self).get_context_data(**kwargs)
        context['usertype'] = "Administrator"
        return context


class MengPOSCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'meng.MEng_Student_Create'
    model = MEngPOS
    form_class = MEngPOSForm
    template_name_suffix = '_meng_form'

    def form_valid(self, form):
        # Sets the owner as the person who created the form
        x =  MEngPOS.objects.filter(((Q(state="AdvisorPending")|Q(state="DGSPending"))&(Q(owner=self.request.user))))
        if (len(x) > 0):
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
            u'Students may only submit a new form if they do not have a current form under review.'
            ])
            return self.form_invalid(form)

        user = self.request.user
        form.instance.owner = user
        form.instance.state = "AdvisorPending"
        return super(MengPOSCreate, self).form_valid(form)


class AdminMengPOSCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'meng.MEng_Admin_Create'
    model = MEngPOS
    form_class = AdminMEngPOSForm
    template_name_suffix = '_meng_form'
    def form_valid(self, form):
        form.instance.state = "AdvisorPending"
        return super(AdminMengPOSCreate, self).form_valid(form)

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
        context = super(AdminMengPOSCreate, self).get_context_data(**kwargs)
        context['usertype'] = "Administrator"
        return context

#Allows Admin to search for forms: HISTORY PAGE
@permission_required('meng.MEng_Admin_View')
def AdminMengPOSsearch(request):
    posfilter = MEngPOSFilter(request.GET, queryset=MEngPOS.objects.all())
    pos_list = posfilter.qs
    type = "MEngPOS"
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

#MEng Function to Delete Forms
@permission_required('meng.MEng_Admin_View')
def mengdelete(request, form_id):
    form = get_object_or_404(MEngPOS, pk=form_id)
    form.delete()
    return redirect('index')


#MEng Function to Approve Forms for Advisors
@permission_required('meng.MEng_Advisor_View')
def mengadvisorapprove(request, form_id):
    form = get_object_or_404(MEngPOS, pk=form_id)
    if ((form.state == "DGSRejected") or (form.state == "Approved")):
        messages.add_message(request, messages.ERROR, "Advisors cannot approve forms already approved or rejected by the DGS.")
        return redirect('advisor-meng-detail', pk=form_id)

    form.state = "DGSPending"
    form.save()
    list = MEngPOS.objects.filter((~Q(pk=form_id))&Q(state="AdvisorPending"))
    if not list:
        return redirect('advisor-meng')
    else:
        return redirect('advisor-meng-detail', pk=list[0])


#Function to Add Comments to MEng Forms for DGS and Reject Form
@permission_required('meng.MEng_Advisor_View')
def mengadvisorcomment(request, form_id):
    object = get_object_or_404(MEngPOS, pk=form_id)
    if ((object.state == "DGSRejected") | (object.state == "Approved")):
        messages.add_message(request, messages.ERROR, "Advisors cannot reject forms already approved or rejected by the DGS.")
        return redirect('advisor-meng-detail', pk=form_id)

    if request.method == "POST":
        form = MEngCommentForm(request.POST)
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
            logger.error("Recipient is:"+recipient)

            first_name = object.owner.first_name
            d = { 'first_name': first_name }

            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


            list = MEngPOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
            if not list:
                return redirect('advisor-meng')
            else:
                return redirect('advisor-meng-detail', pk=list[0])

    else:
        form = MEngCommentForm()
    return render(request, 'comment.html', {'form': form})



#MEng Function to Approve Forms for DGS
@permission_required('meng.MEng_DGS_View')
def mengdgsapprove(request, form_id):
    # form = MEngPOS.objects.get(pk=form_id)
    form = get_object_or_404(MEngPOS, pk=form_id)
    if ((form.state == "AdvisorRejected") or (form.state == "AdvisorPending")):
        messages.add_message(request, messages.ERROR, "The DGS cannot approve forms that haven't been approved by an Advisor.")
        return redirect('dgs-meng-detail', pk=form_id)

    form.state = "Approved"
    form.save()
    recipient = form.owner.email
    logger.error("Recipient:"+recipient)
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

    # send_mail('POS Form Approval', """Your program of study form was fully approved.
    # If you would like to make any changes please submit a new form.
    # From, gradops@ece.duke.edu""", 'gradops@ece.duke.edu', [recipient])
    list = MEngPOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
    if not list:
        return redirect('dgs-meng')
    else:
        return redirect('dgs-meng-detail', pk=list[0])


#Function to Add Comments to MEng Forms for DGS and Reject Form
@permission_required('meng.MEng_DGS_View')
def mengdgscomment(request, form_id):
    object = get_object_or_404(MEngPOS, pk=form_id)
    if ((object.state == "AdvisorRejected") | (object.state == "AdvisorPending")):
        messages.add_message(request, messages.ERROR, "The DGS cannot reject forms that haven't been rejected by an Advisor.")
        return redirect('dgs-meng-detail', pk=form_id)


    if request.method == "POST":
        form = MEngCommentForm(request.POST)
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

            first_name = object.owner.first_name
            recipient = object.owner.email
            logger.error("Recipient is:"+recipient)
            logger.error("First name is:"+first_name)
            d = { 'first_name': first_name }

            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            list = MEngPOS.objects.filter((~Q(pk=form_id))&Q(state="DGSPending"))
            if not list:
                return redirect('dgs-meng')
            else:
                return redirect('dgs-meng-detail', pk=list[0])

    else:
        form = MEngCommentForm()
    return render(request, 'comment.html', {'form': form})

#Function to Return Courses For Given Concentration
def load_courses(request):
    concentration_id = request.GET.get('concentration')
    concentration_entry = Concentration.objects.get(pk=concentration_id)
    courses = Course.objects.filter(concentration=concentration_entry).order_by('listing', 'title')
    return render (request, 'meng/course_dropdown_list_options.html', {'courses': courses})

#Allows DGS to search for forms: HISTORY PAGE
@permission_required('meng.MEng_DGS_View')
def MengPOSsearch(request):
    posfilter = MEngPOSFilter(request.GET, queryset=MEngPOS.objects.filter((Q(state="Approved")|Q(state="DGSRejected"))))
    pos_list = posfilter.qs
    type = "MEngPOS"
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
