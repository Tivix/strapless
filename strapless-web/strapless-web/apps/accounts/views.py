from __future__ import absolute_import

from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .forms import UserDetailsForm


def profile_page(request, username, template='accounts/profile_page.html'):
    context = {}

    if username is None:
        if not request.user.is_authenticated():
            raise Http404()
        context['this_user'] = request.user
    else:
        context['this_user'] = get_object_or_404(get_user_model(), username=username)

    return render(request, template, context)


@login_required
def profile_edit(request, template='accounts/profile_edit.html'):
    d = {}
    if request.method == 'GET':
        form = UserDetailsForm(instance=request.user)
    else:
        form = UserDetailsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()

            user.profile.picture = form.cleaned_data['picture']
            user.profile.save()

            messages.add_message(request, messages.SUCCESS,
                'Your account has been updated')
            return redirect('profile_edit')

    d['form'] = form
    return render(request, template, d)


def login_error(request, template='accounts/login_error.html'):
    d = {}
    return render(request, template, d)
