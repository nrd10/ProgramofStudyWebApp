from import_export import resources
from .models import Person

class CourseResource(resources.ModelResource):
    class Meta:
        model = Course
