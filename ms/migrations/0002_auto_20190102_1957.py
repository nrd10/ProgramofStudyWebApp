# Generated by Django 2.0.8 on 2019-01-02 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shared', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='msthesispos',
            name='electivefour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MStelectiveFour', to='shared.Course', verbose_name='Elective IV'),
        ),
        migrations.AddField(
            model_name='msthesispos',
            name='electiveone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MStelectiveOne', to='shared.Course', verbose_name='Elective I'),
        ),
        migrations.AddField(
            model_name='msthesispos',
            name='electivethree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MStelectiveThree', to='shared.Course', verbose_name='Elective III'),
        ),
        migrations.AddField(
            model_name='msthesispos',
            name='electivetwo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MStelectiveTwo', to='shared.Course', verbose_name='Elective II'),
        ),
        migrations.AddField(
            model_name='msthesispos',
            name='gradececoursefour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MStECEfour', to='shared.Course', verbose_name='Graduate ECE Course IV'),
        ),
        migrations.AddField(
            model_name='msthesispos',
            name='gradececourseone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MStECEone', to='shared.Course', verbose_name='Graduate ECE Course I'),
        ),
        migrations.AddField(
            model_name='msthesispos',
            name='gradececoursethree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MStECEthree', to='shared.Course', verbose_name='Graduate ECE Course III'),
        ),
        migrations.AddField(
            model_name='msthesispos',
            name='gradececoursetwo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MStECEtwo', to='shared.Course', verbose_name='Graduate ECE Course II'),
        ),
        migrations.AddField(
            model_name='msthesispos',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='msthesiscomment',
            name='form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ms.MSThesisPOS'),
        ),
        migrations.AddField(
            model_name='msprojectpos',
            name='electivefive',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MSpelectiveFive', to='shared.Course', verbose_name='Elective V'),
        ),
        migrations.AddField(
            model_name='msprojectpos',
            name='electivefour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MSpelectiveFour', to='shared.Course', verbose_name='Elective IV'),
        ),
        migrations.AddField(
            model_name='msprojectpos',
            name='electiveone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MSpelectiveOne', to='shared.Course', verbose_name='Elective I'),
        ),
        migrations.AddField(
            model_name='msprojectpos',
            name='electivethree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MSpelectiveThree', to='shared.Course', verbose_name='Elective III'),
        ),
        migrations.AddField(
            model_name='msprojectpos',
            name='electivetwo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MSpelectiveTwo', to='shared.Course', verbose_name='Elective II'),
        ),
        migrations.AddField(
            model_name='msprojectpos',
            name='gradececoursefour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MSpECEfour', to='shared.Course', verbose_name='Graduate ECE Course IV'),
        ),
        migrations.AddField(
            model_name='msprojectpos',
            name='gradececourseone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MSpECEone', to='shared.Course', verbose_name='Graduate ECE Course I'),
        ),
        migrations.AddField(
            model_name='msprojectpos',
            name='gradececoursethree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MSpECEthree', to='shared.Course', verbose_name='Graduate ECE Course III'),
        ),
        migrations.AddField(
            model_name='msprojectpos',
            name='gradececoursetwo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MSpECEtwo', to='shared.Course', verbose_name='Graduate ECE Course II'),
        ),
        migrations.AddField(
            model_name='msprojectpos',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='msprojectcomment',
            name='form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ms.MSProjectPOS'),
        ),
        migrations.AddField(
            model_name='mscoursepos',
            name='electivefour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MScelectiveFour', to='shared.Course', verbose_name='Elective IV'),
        ),
        migrations.AddField(
            model_name='mscoursepos',
            name='electiveone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MScelectiveOne', to='shared.Course', verbose_name='Elective I'),
        ),
        migrations.AddField(
            model_name='mscoursepos',
            name='electivethree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MScelectiveThree', to='shared.Course', verbose_name='Elective III'),
        ),
        migrations.AddField(
            model_name='mscoursepos',
            name='electivetwo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MScelectiveTwo', to='shared.Course', verbose_name='Elective II'),
        ),
        migrations.AddField(
            model_name='mscoursepos',
            name='gradececoursefour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MScECEfour', to='shared.Course', verbose_name='Graduate ECE Course IV'),
        ),
        migrations.AddField(
            model_name='mscoursepos',
            name='gradececourseone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MScECEone', to='shared.Course', verbose_name='Graduate ECE Course I'),
        ),
        migrations.AddField(
            model_name='mscoursepos',
            name='gradececoursethree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MScECEthree', to='shared.Course', verbose_name='Graduate ECE Course III'),
        ),
        migrations.AddField(
            model_name='mscoursepos',
            name='gradececoursetwo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MScECEtwo', to='shared.Course', verbose_name='Graduate ECE Course II'),
        ),
        migrations.AddField(
            model_name='mscoursepos',
            name='gradtechcourseone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MScgradtechOne', to='shared.Course', verbose_name='Graduate Technical Elective from ECE or other approved area Course I'),
        ),
        migrations.AddField(
            model_name='mscoursepos',
            name='gradtechcoursetwo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='MScgradtechTwo', to='shared.Course', verbose_name='Graduate Technical Elective from ECE or other approved area Course II'),
        ),
        migrations.AddField(
            model_name='mscoursepos',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mscoursecomment',
            name='form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ms.MSCoursePOS'),
        ),
    ]