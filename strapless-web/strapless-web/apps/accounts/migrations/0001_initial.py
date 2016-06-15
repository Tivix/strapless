# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text=b'Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters', unique=True, max_length=30, verbose_name=b'username', validators=[django.core.validators.RegexValidator(re.compile(b'^[\\w.@+-]+$'), b'Enter a valid username.', b'invalid')])),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name=b'email address')),
                ('first_name', models.CharField(max_length=50, verbose_name=b'first name', blank=True)),
                ('last_name', models.CharField(max_length=50, verbose_name=b'last name', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text=b'Designates whether the user can log into this admin site.', verbose_name=b'staff status')),
                ('is_active', models.BooleanField(default=True, help_text=b'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name=b'active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('newsletter_subscribe', models.BooleanField(default=False)),
                ('picture', models.ImageField(upload_to=b'user_pics/', blank=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
