from import_export import resources
from shared.models import *
from django.conf import settings


class CourseResource(resources.ModelResource):
    class Meta:
        model = Course


class UserResource(resources.ModelResource):
    class Meta:
        model = settings.AUTH_USER_MODEL
