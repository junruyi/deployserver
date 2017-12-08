from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from users.models import User

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'