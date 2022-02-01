from datetime import datetime

from django.utils.text import slugify
import string
import random
import os


def create_random_string(length=30):
    if length <= 0:
        length = 30

    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join([random.choice(symbols) for x in range(length)])

def application_upload(instance, filename):
    now = datetime.now()
    filename_base, filename_ext = os.path.splitext(filename)
    return 'application/{}/{}_{}{}'.format(
        slugify(instance.applicant.user.email),
        now.strftime('%Y%m%d%H%M%S'),
        create_random_string(),
        filename_ext.lower()
    )