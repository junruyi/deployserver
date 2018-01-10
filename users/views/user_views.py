from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import (
    CreateView, UpdateView, FormMixin, FormView
)
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout

from .. import forms
from users.models import User
from ..utils import AdminUserRequiredMixin, user_add_success_next


__all__ = [ 'UserListView', 'UserUpdateView', 'UserDetailView', 'UserProfileView']


class UserListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'users/user_list.html'

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context.update({
            'app': _('Users'),
            'action': _('User list'),
        })
        return context


class UserUpdateView(AdminUserRequiredMixin, UpdateView):
    model = User
    form_class = forms.UserCreateUpdateForm
    template_name = 'users/user_update.html'
    context_object_name = 'user_object'
    success_url = reverse_lazy('users:user-list')

    def form_invalid(self, form):
        username = self.object.username
        user = form.save(commit=False)
        user.username = username
        user.save()
        password = self.request.POST.get('password', '')
        if password:
            user.set_password(password)
        return super(UserUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context.update({'app': _('Users'), 'action': _('Update user')})
        return context


class UserDetailView(AdminUserRequiredMixin, DetailView):
    model = User
    template_name = 'user/user_detail.html'
    content_object_name = 'user_object'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Users'),
            'action': _('User detail'),
        }

        kwargs.update(context)
        return super(UserDetailView, self).get_context_data(**kwargs)


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/user_profile.html'

    def get_context_data(self, **kwargs):

        context = {
            'app': 'User',
            'action': 'User Profile',
        }
        kwargs.update(context)
        return super(UserProfileView, self).get_context_data(**kwargs)