from datetime import datetime

from django.utils.text import slugify
import string
import random
import os
from django import template


def create_random_string(length=30):
    if length <= 0:
        length = 30

    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join([random.choice(symbols) for x in range(length)])


def diploma_upload(instance, filename):
    now = datetime.now()
    filename_base, filename_ext = os.path.splitext(filename)
    return 'diploma/{}/{}_{}{}'.format(
        slugify(instance.applicant.user.email),
        now.strftime('%Y%m%d%H%M%S'),
        create_random_string(),
        filename_ext.lower()
    )

def phd_upload(instance, filename):
    now = datetime.now()
    filename_base, filename_ext = os.path.splitext(filename)
    return 'phd/{}/{}_{}{}'.format(
        slugify(instance.applicant.user.email),
        now.strftime('%Y%m%d%H%M%S'),
        create_random_string(),
        filename_ext.lower()
    )

def job_experience_upload(instance, filename):
    now = datetime.now()
    filename_base, filename_ext = os.path.splitext(filename)
    return 'job_experience/{}/{}_{}{}'.format(
        slugify(instance.applicant.user.email),
        now.strftime('%Y%m%d%H%M%S'),
        create_random_string(),
        filename_ext.lower()
    )

def reference_upload(instance, filename):
    now = datetime.now()
    filename_base, filename_ext = os.path.splitext(filename)
    return 'reference/{}/{}_{}{}'.format(
        slugify(instance.applicant.user.email),
        now.strftime('%Y%m%d%H%M%S'),
        create_random_string(),
        filename_ext.lower()
    )

def application_upload(instance, filename):
    now = datetime.now()
    filename_base, filename_ext = os.path.splitext(filename)
    return 'application/{}/{}_{}{}'.format(
        slugify(instance.applicant.user.email),
        now.strftime('%Y%m%d%H%M%S'),
        create_random_string(),
        filename_ext.lower()
    )