from django.shortcuts import redirect
from django.core.exceptions import ImproperlyConfigured
import os


def get_env_value(env_variable):
    try:
        return os.environ[env_variable]
    except KeyError:
        error_msg = f'Set the {env_variable} environment variable'
        raise ImproperlyConfigured(error_msg)


def redirect_news(request):
    return redirect('home', permanent=True)
