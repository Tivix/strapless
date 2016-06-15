from __future__ import absolute_import

from django import forms
from django.contrib.auth.forms import (
    UserCreationForm as BaseUserCreationForm,
    UserChangeForm as BaseUserChangeForm)

from allauth.account.forms import SignupForm as BaseSignupForm

from .models import User


class SignupForm(BaseSignupForm):
    """Capture other details represented in UserProfile and custom User models."""
    first_name = forms.CharField(label='First Name', max_length=50)
    last_name = forms.CharField(label='Last Name', max_length=50)
    email = forms.EmailField(label='E-mail', max_length=254)
    tos = forms.BooleanField(label='Accept the terms of service')
    newsletter_subscribe = forms.BooleanField(required=False)

    RESERVED_USERNAMES = ['admin', 'search', 'uploads', 'static', 'media', 'edit']

    def clean_username(self):
        super(SignupForm, self).clean_username()
        username = self.cleaned_data.get('username')
        if username in self.RESERVED_USERNAMES:
            raise forms.ValidationError('This username is already taken.')
        if len(username) < 5:
            raise forms.ValidationError('Usernames should be at least 5 characters long.')
        return username

    def save(self, request):
        user = super(SignupForm, self).save(request)
        # Store the common profile data.
        user.profile.newsletter_subscribe = self.cleaned_data['newsletter_subscribe']
        user.profile.save()
        return user


class UserDetailsForm(forms.ModelForm):
    """Used when users want to edit their details."""
    picture = forms.ImageField(required=False)

    class Meta:
        model = User  # This form is specific to this exact model so no get_user_model()
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserDetailsForm, self).__init__(*args, **kwargs)
        user = kwargs.get('instance')

        # These fields are set to blank=True in user model, override this.
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        if user and user.profile.picture:
            self.fields['picture'].initial = user.profile.picture


class UserCreationForm(BaseUserCreationForm):
    """
    Customized UserCreationForm for admin panel, based on original User form.

    See custom User model docstring for details.
    """

    class Meta(BaseUserCreationForm.Meta):
        model = User  # This form is specific to this exact model so no get_user_model()
        fields = ('username', 'email')

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )


class UserChangeForm(BaseUserChangeForm):
    """
    Customized UserChangeForm for admin panel, based on original User form.

    See custom User model docstring for details.
    """

    class Meta(BaseUserChangeForm.Meta):
        model = User  # This form is specific to this exact model so no get_user_model()
