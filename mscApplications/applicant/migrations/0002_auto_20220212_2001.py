# Generated by Django 3.2.3 on 2022-02-12 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diploma',
            name='type',
            field=models.CharField(choices=[('UG', 'Undergraduate'), ('PG', 'Postgraduate')], max_length=2, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='phd',
            name='type',
            field=models.CharField(choices=[('UG', 'Undergraduate'), ('PG', 'Postgraduate')], max_length=2, verbose_name='Type'),
        ),
    ]
