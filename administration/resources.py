from import_export import fields, resources
from shared.models import Course, CourseType
from shared.models import User
from django.contrib.auth.models import Group
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from django.db.models import Q #allows for complex queries
import logging
from django.conf import settings
logger = logging.getLogger('administration/resources.py')


class UserResource(resources.ModelResource):
    advisor_real = fields.Field(
        column_name='advisor',
        attribute='advisor',
        widget=ForeignKeyWidget(User, 'netid'))

    group_real = fields.Field(
        column_name='groups',
        attribute='groups',
        widget=ManyToManyWidget(Group, ',', 'name'))

    class Meta:
        model = User
        import_id_field = ['id']
        import_id_field = ('id',)
        fields = ('id', 'netid', 'email', 'first_name', 'last_name', 'student_id', 'user_type', 'advisor_real', 'group_real')
        skip_unchanged = True
        report_skipped = False

class CourseResource(resources.ModelResource):
    category1 = fields.Field(
        column_name='category',
        attribute='category',
        widget=ManyToManyWidget(CourseType, ',', 'title'))

    class Meta:
        model = Course
        import_id_field = ['id']
        import_id_field = ('id',)
        fields = ('id', 'listing', 'title', 'category1', 'concentration', 'term')
        skip_unchanged = True
        report_skipped = False


class CourseUpdate(resources.ModelResource):
    category1 = fields.Field(
        column_name='category',
        attribute='category',
        widget=ManyToManyWidget(CourseType, ',', 'title'))

    class Meta:
        model = Course
        import_id_field = ['id']
        import_id_field = ('id',)
        fields = ('id', 'listing', 'title', 'category1', 'concentration', 'term')
        skip_unchanged = True
        report_skipped = False


    #Using this method to Update Rows; Don't Want New Rows Made for Same Listing
    def skip_row(self, instance, original):
        instance_listing_value = getattr(instance, 'listing')
        # logger.info("My listing is:"+instance_listing_value)
        objects= Course.objects.filter(Q(listing__iexact=instance_listing_value))
        if (not objects):
            logger.error("OBJECT IS NONE --> IMPORT CLASS NOT THERE!")
            return False
        object = objects.first()
        # logger.info(object)

        # Get Object attributes of interest
        listing = object.listing
        attributes = [object.title, object.term]
        if not self._meta.skip_unchanged:
            return False

        mylist = (self.get_fields())
        #Empty list of fields to check for changes
        fieldlist = []
        fieldlist.append(mylist[3])
        fieldlist.append(mylist[5])
        counter = 0
        for item in fieldlist:
            instance_field = item.get_value(instance)
            logger.info("Instance item is:"+instance_field)
            logger.info("Object item is:"+attributes[counter])
            if (instance_field != attributes[counter]):
                logger.info("Unequal Fields --> CHANGE FIELD")
                if counter == 0:
                    object.title = instance_field
                else:
                    object.term = instance_field
                object.save()
            counter += 1

        return True
