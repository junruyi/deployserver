
from __future__ import unicode_literals
from django import forms
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render ,reverse,redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from formtools.wizard.views import SessionWizardView
from django.conf import settings

from users.models import User
from users import forms
from ..utils import AdminUserRequiredMixin

__all__ = ['UserLoginView']

@method_decorator(sensitive_post_parameters(), name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class UserLoginView(FormView):
    template_name = 'users/login.html'
    form_class = forms.UserLoginForm
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect(self.get_success_url())
        return super(UserLoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        login_ip = self.request.META.get('REMOTE_ADDR', '')
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        #write_login_log_async.delay(self.request.user.username,
        #                            self.request.user.name,
        #                            login_type='W', login_ip=login_ip,
        #                            user_agent=user_agent
        #                            )
        return redirect(self.get_success_url())

    def get_success_url(self):
        return self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, reverse('index'))
        )


class UserListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'users/user_list.html'

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context.update({
            'app': _('Users'),
            'action': _('User list'),
        })
        return context


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/user_profile.html'

    def get_context_data(self, **kwargs):

        context = {
            'app': 'User',
            'action': 'User Profile',
        }
        kwargs.update(context)
        return super(UserProfileView, self).get_context_data(**kwargs)