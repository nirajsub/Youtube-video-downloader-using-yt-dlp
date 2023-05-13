

from .views import *
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('', index, name='home'),
    path('', SetLanguage, name="setlanguage")
]

