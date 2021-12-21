from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def check_user(type):
    def user_type(u):
        if u.is_authenticated:
            if type==1 and u.is_applicant or type==2 and u.is_evaluator:
                return True
        raise PermissionDenied

    return user_passes_test(user_type)