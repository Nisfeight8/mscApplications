# Generated by Django 3.2.3 on 2021-12-30 17:40

from django.db import migrations, models
import django.db.models.deletion
import evaluator.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institution', '0001_initial'),
        ('user_account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluator',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='evaluator', serialize=False, to='user_account.user')),
                ('telephone', models.CharField(max_length=10, validators=[evaluator.validators.only_int], verbose_name='Telephone')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='institution.department')),
            ],
        ),
    ]
