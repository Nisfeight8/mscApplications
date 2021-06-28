# Generated by Django 3.2.3 on 2021-06-16 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        #('auth', '0013_alter_user_email'),
        ('institution', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('end_date', models.DateField(verbose_name='End Date')),
            ],
        ),
        migrations.CreateModel(
            name='MscProgramme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('address', models.CharField(max_length=50, verbose_name='Address')),
                ('pobox', models.CharField(max_length=5, verbose_name='Pobox')),
                ('city', models.CharField(max_length=64, verbose_name='City')),
                ('country', models.CharField(max_length=50, verbose_name='Country')),
                ('telephone', models.CharField(max_length=10, verbose_name='Telephone')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institution.department', verbose_name='Department')),
            ],
        ),
        migrations.CreateModel(
            name='MscFlow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('msc_programme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msc.mscprogramme', verbose_name='Programme')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluator',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='evaluator', serialize=False, to='auth.user', verbose_name='User')),
                ('telephone', models.CharField(max_length=10, verbose_name='Telephone')),
                ('committee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='msc.call', verbose_name='Committe')),
            ],
        ),
        migrations.AddField(
            model_name='call',
            name='msc_programme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msc.mscprogramme', verbose_name='Programe'),
        ),
    ]
