# Generated by Django 3.2.3 on 2021-06-16 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institution', '0005_auto_20210616_1400'),
        ('msc', '0003_auto_20210616_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='call',
            name='msc_programme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msc.mscprogramme'),
        ),
        migrations.AlterField(
            model_name='call',
            name='start_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='call',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='call',
            name='title_el_GR',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='call',
            name='title_en_us',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='evaluator',
            name='committee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='msc.call'),
        ),
        migrations.AlterField(
            model_name='evaluator',
            name='telephone',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='evaluator',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='evaluator', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mscflow',
            name='msc_programme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msc.mscprogramme'),
        ),
        migrations.AlterField(
            model_name='mscflow',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='mscflow',
            name='title_el_GR',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='mscflow',
            name='title_en_us',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='mscprogramme',
            name='address',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='mscprogramme',
            name='address_el_GR',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='mscprogramme',
            name='address_en_us',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='mscprogramme',
            name='city',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='mscprogramme',
            name='city_el_GR',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='mscprogramme',
            name='city_en_us',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='mscprogramme',
            name='country',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='mscprogramme',
            name='country_el_GR',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='mscprogramme',
            name='country_en_us',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='mscprogramme',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institution.department'),
        ),
        migrations.AlterField(
            model_name='mscprogramme',
            name='pobox',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='mscprogramme',
            name='telephone',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='mscprogramme',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='mscprogramme',
            name='title_el_GR',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='mscprogramme',
            name='title_en_us',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
