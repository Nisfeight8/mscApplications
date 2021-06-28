# Generated by Django 3.2.3 on 2021-06-16 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('address', models.CharField(max_length=50, verbose_name='Address')),
                ('pobox', models.CharField(max_length=5, verbose_name='Pobox')),
                ('city', models.CharField(max_length=64, verbose_name='City')),
                ('country', models.CharField(max_length=50, verbose_name='Country')),
                ('telephone', models.CharField(max_length=10, verbose_name='Telephone')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('address', models.CharField(max_length=50, verbose_name='Address')),
                ('pobox', models.CharField(max_length=5, verbose_name='Pobox')),
                ('city', models.CharField(max_length=64, verbose_name='City')),
                ('country', models.CharField(max_length=50, verbose_name='Country')),
                ('telephone', models.CharField(max_length=10, verbose_name='Telephone')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institution.institution', verbose_name='Institution')),
            ],
        ),
    ]
