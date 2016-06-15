from __future__ import absolute_import
import re

from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.core.mail import send_mail
from django.utils import timezone
from django.core import validators
from django.dispatch import receiver


class UserManager(BaseUserManager):
    """
    Based on Django's original UserManager.

    See custom User's docstring for details.
    Source code taken from:
    https://github.com/django/django/blob/stable/1.6.x/django/contrib/auth/models.py#L170
    """

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Customized User model based on Django's original User.

    Contains fixes like longer email (75 -> 254 which is RFC standard),
    e-mail uniqueness, longer first_name and last_name.

    Source code taken from:
    https://github.com/django/django/blob/stable/1.6.x/django/contrib/auth/models.py#L361

    See docs for the details how to handle with this:
    https://docs.djangoproject.com/en/dev/topics/auth/customizing/#substituting-a-custom-user-model

    NOTE If changing specs of the custom User (e.g. setting email as a username),
        be sure to adjust other places also, like UserManager,
        UserCreationForm and UserChangeForm (from admin panel), UserAdmin
        panel, registration forms, etc. See above docs link for details.
    """

    username = models.CharField('username', max_length=30, unique=True,
        help_text='Required. 30 characters or fewer. Letters, numbers and '
                  '@/./+/-/_ characters',
        validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'), 'Enter a valid username.', 'invalid')
        ])
    email = models.EmailField('email address', max_length=254, unique=True)
    first_name = models.CharField('first name', max_length=50, blank=True)
    last_name = models.CharField('last name', max_length=50, blank=True)

    is_staff = models.BooleanField('staff status', default=False,
        help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField('active', default=True,
        help_text='Designates whether this user should be treated as '
                  'active. Unselect this instead of deleting accounts.')

    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __unicode__(self):
        return self.get_username()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between
        [upstream AbstractUser method].
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user [upstream AbstractUser method]."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User [upstream AbstractUser method]."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

@receiver(post_save, sender=User, dispatch_uid='create_user_profile')
def create_user_profile(sender, **kwargs):
    """Automatically create UserProfile for newly created, non-raw User."""
    # If save is "raw" (coming from a fixture), don't create profile--
    # it should be manually specified in a fixture along with User object.
    if kwargs.get('created', True) and not kwargs.get('raw', False):
        UserProfile.objects.create(user=kwargs.get('instance'))


class UserProfile(models.Model):
    """Profile for User, automatically created in User.save()."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    newsletter_subscribe = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='user_pics/', blank=True)

    def __unicode__(self):
        return "%s's profile" % self.user
