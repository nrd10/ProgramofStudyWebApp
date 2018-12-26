# Generated by Django 2.0.6 on 2018-12-26 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MSCourseComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(help_text='Please enter a comment explaining why this form is being rejected.', max_length=2000)),
                ('authortype', models.CharField(blank=True, choices=[('Advisor', 'Advisor'), ('DGS', 'DGS')], help_text='Either DGS or Advisor Commenting', max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Course Comments',
                'verbose_name': 'Course Comment',
            },
        ),
        migrations.CreateModel(
            name='MSCoursePOS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gradeceoneterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('gradeceonegrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('gradecetwoterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('gradecetwograde', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('gradecethreeterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('gradecethreegrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('gradecefourterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('gradecefourgrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('gradtechoneterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('gradtechonegrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('gradtechtwoterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('gradtechtwograde', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('electiveoneterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('electiveonegrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('electivetwoterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('electivetwograde', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('electivethreeterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('electivethreegrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('electivefourterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('electivefourgrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('submission', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(blank=True, choices=[('New', 'New'), ('AdvisorRejected', 'AdvisorRejected'), ('DGSRejected', 'DGSRejected'), ('AdvisorPending', 'AdvisorPending'), ('DGSPending', 'DGSPending'), ('Approved', 'Approved')], default=('New', 'New'), help_text='POS Form State', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Coursework MS Forms',
                'permissions': (('MSc_Student_View', 'Student View MS Coursework Forms'), ('MSc_Student_Create', 'Student Create MS Coursework Forms'), ('MSc_Advisor_View', 'Advisor View MS Coursework Forms'), ('MSc_DGS_View', 'DGS View MS Coursework Forms'), ('MSc_Admin_View', 'Admin View MS Coursework Forms'), ('MSc_Admin_Create', 'Admin Create MS Coursework Forms')),
                'verbose_name': 'Coursework MS Form',
            },
        ),
        migrations.CreateModel(
            name='MSProjectComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(help_text='Please enter a comment explaining why this form is being rejected.', max_length=2000)),
                ('authortype', models.CharField(blank=True, choices=[('Advisor', 'Advisor'), ('DGS', 'DGS')], help_text='Either DGS or Advisor Commenting', max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Project Comments',
                'verbose_name': 'Project Comment',
            },
        ),
        migrations.CreateModel(
            name='MSProjectPOS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gradeceoneterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('gradeceonegrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('gradecetwoterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('gradecetwograde', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('gradecethreeterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('gradecethreegrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('gradecefourterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('gradecefourgrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('electiveoneterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('electiveonegrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('electivetwoterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('electivetwograde', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('electivethreeterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('electivethreegrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('electivefourterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('electivefourgrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('electivefiveterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('electivefivegrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('researchcourseterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('SUMMER 2018', 'SUMMER 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('SUMMER 2019', 'SUMMER 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('SUMMER 2020', 'SUMMER 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021'), ('SUMMER 2021', 'SUMMER 2021')], default=('FALL 2018', 'FALL 2018'), max_length=20, verbose_name='Research Credit I Term')),
                ('researchcoursegrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('submission', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(blank=True, choices=[('New', 'New'), ('AdvisorRejected', 'AdvisorRejected'), ('DGSRejected', 'DGSRejected'), ('AdvisorPending', 'AdvisorPending'), ('DGSPending', 'DGSPending'), ('Approved', 'Approved')], default=('New', 'New'), help_text='POS Form State', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Project MS Forms',
                'permissions': (('MSp_Student_View', 'Student View MS Project Forms'), ('MSp_Student_Create', 'Student Create MS Project Forms'), ('MSp_Advisor_View', 'Advisor View MS Project Forms'), ('MSp_DGS_View', 'DGS View MS Project Forms'), ('MSp_Admin_View', 'Admin View MS Project Forms'), ('MSp_Admin_Create', 'Admin Create MS Project Forms')),
                'verbose_name': 'Project MS Form',
            },
        ),
        migrations.CreateModel(
            name='MSThesisComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(help_text='Please enter a comment explaining why this form is being rejected.', max_length=2000)),
                ('authortype', models.CharField(blank=True, choices=[('Advisor', 'Advisor'), ('DGS', 'DGS')], help_text='Either DGS or Advisor Commenting', max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Thesis Comments',
                'verbose_name': 'Thesis Comment',
            },
        ),
        migrations.CreateModel(
            name='MSThesisPOS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gradeceoneterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('gradeceonegrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('gradecetwoterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('gradecetwograde', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('gradecethreeterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('gradecethreegrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('gradecefourterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('gradecefourgrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('electiveoneterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('electiveonegrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('electivetwoterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('electivetwograde', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('electivethreeterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('electivethreegrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('electivefourterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021')], default=('FALL 2018', 'FALL 2018'), max_length=30, verbose_name='Term')),
                ('electivefourgrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('researchcourseterm', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('SUMMER 2018', 'SUMMER 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('SUMMER 2019', 'SUMMER 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('SUMMER 2020', 'SUMMER 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021'), ('SUMMER 2021', 'SUMMER 2021')], default=('FALL 2018', 'FALL 2018'), max_length=20, verbose_name='Research Credit Semester I')),
                ('researchcoursegrade', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('researchcoursetermtwo', models.CharField(choices=[('FALL 2018', 'FALL 2018'), ('SPRING 2018', 'SPRING 2018'), ('SUMMER 2018', 'SUMMER 2018'), ('FALL 2019', 'FALL 2019'), ('SPRING 2019', 'SPRING 2019'), ('SUMMER 2019', 'SUMMER 2019'), ('FALL 2020', 'FALL 2020'), ('SPRING 2020', 'SPRING 2020'), ('SUMMER 2020', 'SUMMER 2020'), ('FALL 2021', 'FALL 2021'), ('SPRING 2021', 'SPRING 2021'), ('SUMMER 2021', 'SUMMER 2021')], default=('FALL 2018', 'FALL 2018'), max_length=20, verbose_name='Research Credit Semester II')),
                ('researchcoursetwograde', models.CharField(blank=True, choices=[('A+', 'A+'), ('A', 'A'), ('A-', 'A-'), ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'), ('C+', 'C+'), ('C', 'C'), ('C-', 'C-')], max_length=5, verbose_name='Grade')),
                ('submission', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(blank=True, choices=[('New', 'New'), ('AdvisorRejected', 'AdvisorRejected'), ('DGSRejected', 'DGSRejected'), ('AdvisorPending', 'AdvisorPending'), ('DGSPending', 'DGSPending'), ('Approved', 'Approved')], default=('New', 'New'), help_text='POS Form State', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Thesis MS Forms',
                'permissions': (('MSt_Student_View', 'Student View MS Thesis Forms'), ('MSt_Student_Create', 'Student Create MS Thesis Forms'), ('MSt_Advisor_View', 'Advisor View MS Thesis Forms'), ('MSt_DGS_View', 'DGS View MS Thesis Forms'), ('MSt_Admin_View', 'Admin View MS Thesis Forms'), ('MSt_Admin_Create', 'Admin Create MS Thesis Forms')),
                'verbose_name': 'Thesis MS Form',
            },
        ),
    ]
