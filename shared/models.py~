from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.urls import reverse
from multiselectfield import MultiSelectField

#Import User Manager
from .managers import UserManager


#User Types
POSTYPE = []
POSTYPE.append(("MEng", "MEng"))
POSTYPE.append(("MS", "MS"))
POSTYPE.append(("PhD", "PhD"))
POSTYPE.append(("Advisor", "Advisor"))
POSTYPE.append(("DGS", "DGS"))
POSTYPE.append(("Administrator", "Administrator"))

POSTYPE_MULTI = []
POSTYPE_MULTI.append((1, "MEng"))
POSTYPE_MULTI.append((2, "MS"))
POSTYPE_MULTI.append((3, "PhD"))
POSTYPE_MULTI.append((4, "Advisor"))
POSTYPE_MULTI.append((5, "DGS"))
POSTYPE_MULTI.append((6, "Administrator"))


#Term Types
TERM = []
TERM.append(("FALL", "FALL"))
TERM.append(("SPRING", "SPRING"))
TERM.append(("SUMMER", "SUMMER"))
TERM.append(("FALL-SPRNG", "FALL-SPRNG"))
TERM.append(("FA-SPR-SU", "FA-SPR-SU"))
TERM.append(("OCCASIONAL", "OCCASIONAL"))
TERM.append(("UNKNOWN", "UNKNOWN"))

class User(AbstractBaseUser, PermissionsMixin):
    netid = models.CharField(_('netid'), max_length=30, unique=True)
    email = models.EmailField(_('email address'), max_length=30)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    student_id = models.IntegerField(_('student id'), default=1)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    # user_type = models.CharField(max_length=20, choices=POSTYPE, blank=True, default=POSTYPE[0], help_text='User Type')
    user_type = MultiSelectField(max_length=20, choices=POSTYPE, max_choices=4)
    advisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, null=True, blank=True, related_name="Advisor")
    objects = UserManager()

    USERNAME_FIELD = 'netid'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'student_id']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        permissions = (("User_Admin_Create", "Admin Create Users"),)

    def __str__(self):
        return self.netid

    def get_absolute_url(self):
        '''
        Returns the url to access a particular instance of the model.
        '''
        return reverse('admin-user-detail', args=[str(self.id)])

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def get_netid(self):
        '''
        Returns the netid for the user.
        '''
        return self.netid

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        if (self.email is not None):
            send_mail(subject, message, from_email, [self.email], **kwargs)

class Course(models.Model):
    '''
    Model for representing each course
    '''
    listing = models.CharField(max_length=100, help_text="Enter the numeric listing for a current course (e.g. MEng 540).")
    title = models.CharField(max_length=100, default="Example Class", help_text="Enter the full name of the course")
    category = models.ManyToManyField('CourseType', blank=True)
    concentration = models.ManyToManyField('Concentration', blank=True)
    term = models.CharField(max_length=30, choices=TERM, blank=True, help_text='Semester')

    class Meta:
        ordering = ['-id']
        permissions = (("Course_Admin_Create", "Admin Create Courses"),)


    def __str__(self):
        '''
        String to represent this object
        '''
        return '%s: %s' % (self.listing, self.title)

    def display_concentration(self):
        """
        Creates a string for the Concentration. This is required to display genre in Admin.
        """
        return ', '.join([ concentration.title for concentration in self.concentration.all()[:3] ])

    display_concentration.short_description = 'Concentration'

    def display_category(self):
        """
        Creates a string for the Category. This is required to display genre in Admin.
        """
        return ', '.join([ category.title for category in self.category.all()[:3] ])

    display_category.short_description = 'Course Category'


    def get_absolute_url(self):
        '''
        Returns the url to access a particular instance of the model for
        Admin view.
        '''
        return reverse('admin-course-detail', args=[str(self.id)])


class Concentration(models.Model):
    '''
    Model for representing each Concentration Area
    '''
    title = models.CharField(max_length=100, help_text="Enter a Concentration Area (e.g. Photonics, Computer Architecture, etc.)")

    def __str__(self):
        '''
        String to represent this object
        '''
        return self.title


class CourseType(models.Model):
    '''
    Model for listing categories for each course
    '''
    title = models.CharField(max_length=100, help_text="Enter a course category (e.g. Core Industry Prep, ECE Technical Course, etc.)")

    def __str__(self):
        '''
        String to represent this object
        '''
        return self.title

    class Meta:
        verbose_name = 'Course Category'
        verbose_name_plural = 'Course Categories'

# CREATE GROUPS: each group will have some subset of the permissions for each class
MEng_students, created = Group.objects.get_or_create(name = 'MEng_students')
MS_students = Group.objects.get_or_create(name = 'MS_students')
Advisor_group = Group.objects.get_or_create(name = 'Advisor_group')
DGS_group = Group.objects.get_or_create(name = 'DGS_group')
PHD_students = Group.objects.get_or_create(name = 'PHD_students')
Administrators = Group.objects.get_or_create(name = 'Administrators')
