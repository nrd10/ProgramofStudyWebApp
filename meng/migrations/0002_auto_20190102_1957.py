# Generated by Django 2.0.8 on 2019-01-02 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('meng', '0001_initial'),
        ('shared', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='mengpos',
            name='concentration',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shared.Concentration'),
        ),
        migrations.AddField(
            model_name='mengpos',
            name='coreclassone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Mengcoreone', to='shared.Course', verbose_name='Core Industry Prep Course I'),
        ),
        migrations.AddField(
            model_name='mengpos',
            name='coreclasstwo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Mengcoretwo', to='shared.Course', verbose_name='Core Industry Prep Course II'),
        ),
        migrations.AddField(
            model_name='mengpos',
            name='electiveone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MEngelectiveOne', to='shared.Course', verbose_name='Elective I'),
        ),
        migrations.AddField(
            model_name='mengpos',
            name='electivethree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MEngelectiveThree', to='shared.Course', verbose_name='Elective III'),
        ),
        migrations.AddField(
            model_name='mengpos',
            name='electivetwo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MEngelectiveTwo', to='shared.Course', verbose_name='Elective II'),
        ),
        migrations.AddField(
            model_name='mengpos',
            name='gradtechcourseone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MEnggradtechOne', to='shared.Course', verbose_name='Graduate Technical Elective from ECE or other approved area Course I'),
        ),
        migrations.AddField(
            model_name='mengpos',
            name='gradtechcoursetwo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MEnggradtechTwo', to='shared.Course', verbose_name='Graduate Technical Elective from ECE or other approved area Course II'),
        ),
        migrations.AddField(
            model_name='mengpos',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mengpos',
            name='techcourseone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MEngtechONE', to='shared.Course', verbose_name='Concentration Area Course I'),
        ),
        migrations.AddField(
            model_name='mengpos',
            name='techcoursethree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MEngtechThree', to='shared.Course', verbose_name='Concentration Course III'),
        ),
        migrations.AddField(
            model_name='mengpos',
            name='techcoursetwo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MEngtechTWO', to='shared.Course', verbose_name='Concentration Area Course II '),
        ),
        migrations.AddField(
            model_name='mengcomment',
            name='form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='meng.MEngPOS'),
        ),
        migrations.AddField(
            model_name='mengcomment',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
