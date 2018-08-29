# Generated by Django 2.0.6 on 2018-08-29 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields
import shared.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('netid', models.CharField(max_length=30, unique=True, verbose_name='netid')),
                ('email', models.EmailField(max_length=30, verbose_name='email address')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
                ('student_id', models.IntegerField(default=1, verbose_name='student id')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('user_type', multiselectfield.db.fields.MultiSelectField(choices=[('MEng', 'MEng'), ('MS', 'MS'), ('PhD', 'PhD'), ('Advisor', 'Advisor'), ('DGS', 'DGS'), ('Administrator', 'Administrator')], max_length=20)),
                ('advisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Advisor', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'permissions': (('User_Admin_Create', 'Admin Create Users'),),
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', shared.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Concentration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter a Concentration Area (e.g. Photonics, Computer Architecture, etc.)', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.CharField(help_text='Enter the numeric listing for a current course (e.g. MEng 540).', max_length=100)),
                ('title', models.CharField(default='Example Class', help_text='Enter the full name of the course', max_length=100)),
                ('term', models.CharField(blank=True, choices=[('FALL', 'FALL'), ('SPRING', 'SPRING'), ('SUMMER', 'SUMMER'), ('FALL-SPRNG', 'FALL-SPRNG'), ('FA-SPR-SU', 'FA-SPR-SU'), ('OCCASIONAL', 'OCCASIONAL'), ('UNKNOWN', 'UNKNOWN')], help_text='Semester', max_length=30)),
            ],
            options={
                'ordering': ['-id'],
                'permissions': (('Course_Admin_Create', 'Admin Create Courses'),),
            },
        ),
        migrations.CreateModel(
            name='CourseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter a course category (e.g. Core Industry Prep, ECE Technical Course, etc.)', max_length=100)),
            ],
            options={
                'verbose_name': 'Course Category',
                'verbose_name_plural': 'Course Categories',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ManyToManyField(blank=True, to='shared.CourseType'),
        ),
        migrations.AddField(
            model_name='course',
            name='concentration',
            field=models.ManyToManyField(blank=True, to='shared.Concentration'),
        ),
    ]
