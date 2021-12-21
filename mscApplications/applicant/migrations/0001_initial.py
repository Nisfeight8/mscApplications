# Generated by Django 3.2.3 on 2021-12-21 14:02

import applicant.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_account', '0001_initial'),
        ('msc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='applicant', serialize=False, to='user_account.user', verbose_name='User')),
                ('telephone', models.CharField(max_length=10, validators=[applicant.validators.only_int], verbose_name='Telephone')),
                ('address', models.CharField(max_length=50, verbose_name='Address')),
                ('city', models.CharField(max_length=64, verbose_name='City')),
                ('country', models.CharField(max_length=50, verbose_name='Country')),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, verbose_name='Gender')),
                ('citizenship', models.CharField(max_length=64, verbose_name='Citizenship')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateField(auto_now_add=True, verbose_name='Submission Date')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Comments')),
                ('admitted', models.BooleanField(blank=True, default=None, null=True, verbose_name='Admitted')),
                ('media_file', models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Media File')),
                ('admitted_flow', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admitted_application', to='msc.mscflow', verbose_name='Admitted FLow')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicant.applicant')),
                ('call', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msc.call')),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.CharField(max_length=200, verbose_name='Organization')),
                ('city', models.CharField(max_length=64, verbose_name='City')),
                ('country', models.CharField(max_length=50, verbose_name='Country')),
                ('job_title', models.CharField(max_length=200, verbose_name='Job Title')),
                ('first_name', models.CharField(max_length=30, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('telephone', models.CharField(max_length=10, verbose_name='Telephone')),
                ('reference_date', models.DateField(verbose_name='Reference Date')),
                ('media_file', models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Media File')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicant.applicant', verbose_name='Applicant')),
            ],
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.PositiveIntegerField(verbose_name='Priority')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicant.application', verbose_name='Application')),
                ('flow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msc.mscflow', verbose_name='Flow')),
            ],
            options={
                'ordering': ['priority'],
            },
        ),
        migrations.CreateModel(
            name='Phd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('', ''), ('', ''), ('UG', 'Undergraduate'), ('PG', 'Postgraduate')], max_length=2, verbose_name='Type')),
                ('awarding_institution', models.CharField(max_length=200, verbose_name='Awarding Institution')),
                ('department', models.CharField(max_length=200, verbose_name='Department')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('supervisor', models.CharField(max_length=64, verbose_name='Supervisor')),
                ('date_awarded', models.DateField(verbose_name='Date Awarded')),
                ('grade_point_average', models.CharField(max_length=2, verbose_name='Average Grade')),
                ('city', models.CharField(max_length=64, verbose_name='City')),
                ('country', models.CharField(max_length=50, verbose_name='Country')),
                ('media_file', models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Media File')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicant.applicant', verbose_name='Applicant')),
            ],
        ),
        migrations.CreateModel(
            name='JobExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.CharField(max_length=200, verbose_name='Organization')),
                ('city', models.CharField(max_length=64, verbose_name='City')),
                ('country', models.CharField(max_length=50, verbose_name='Country')),
                ('job_title', models.CharField(max_length=200, verbose_name='Job Title')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('media_file', models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Media File')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicant.applicant', verbose_name='Applicant')),
            ],
        ),
        migrations.CreateModel(
            name='Diploma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('', ''), ('', ''), ('UG', 'Undergraduate'), ('PG', 'Postgraduate')], max_length=2, verbose_name='Type')),
                ('awarding_institution', models.CharField(max_length=200, verbose_name='Awarding Institution')),
                ('department', models.CharField(max_length=200, verbose_name='Department')),
                ('specialization', models.CharField(blank=True, max_length=100, null=True, verbose_name='Specialization')),
                ('date_awarded', models.DateField(verbose_name='Date Awarded')),
                ('grade_point_average', models.CharField(max_length=2, verbose_name='Average Grade')),
                ('city', models.CharField(max_length=64, verbose_name='City')),
                ('country', models.CharField(max_length=50, verbose_name='Country')),
                ('media_file', models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Media File')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicant.applicant', verbose_name='Applicant')),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='preferences',
            field=models.ManyToManyField(blank=True, related_name='waiting_applications', through='applicant.Preference', to='msc.MscFlow', verbose_name='Preferences'),
        ),
        migrations.AddField(
            model_name='application',
            name='reference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='applicant.reference', verbose_name='Reference'),
        ),
    ]
