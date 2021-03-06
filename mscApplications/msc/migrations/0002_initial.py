# Generated by Django 3.2.3 on 2022-02-01 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('msc', '0001_initial'),
        ('evaluator', '0001_initial'),
        ('applicant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='evaluators',
            field=models.ManyToManyField(to='evaluator.Evaluator'),
        ),
        migrations.AddField(
            model_name='call',
            name='msc_programme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msc.mscprogramme', verbose_name='Msc Programme'),
        ),
        migrations.AddField(
            model_name='application',
            name='admitted_flow',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admitted_application', to='msc.mscflow'),
        ),
        migrations.AddField(
            model_name='application',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicant.applicant'),
        ),
        migrations.AddField(
            model_name='application',
            name='call',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msc.call'),
        ),
        migrations.AddField(
            model_name='application',
            name='preferences',
            field=models.ManyToManyField(blank=True, related_name='waiting_applications', through='msc.Preference', to='msc.MscFlow'),
        ),
        migrations.AddField(
            model_name='application',
            name='reference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='applicant.reference'),
        ),
    ]
