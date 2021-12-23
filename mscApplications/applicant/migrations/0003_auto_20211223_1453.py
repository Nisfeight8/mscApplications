# Generated by Django 3.2.3 on 2021-12-23 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0002_auto_20211222_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diploma',
            name='type',
            field=models.CharField(choices=[('', ''), ('', ''), ('UG', 'Undergraduate'), ('PG', 'Postgraduate')], default='UG', max_length=2, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='phd',
            name='type',
            field=models.CharField(choices=[('', ''), ('', ''), ('UG', 'Undergraduate'), ('PG', 'Postgraduate')], default='UG', max_length=2, verbose_name='Type'),
        ),
    ]
