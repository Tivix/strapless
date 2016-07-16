# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.core import management


def load_initial_data(apps, schema_editor):
    # Since Django 1.7 initial_data fixtures are not loaded automatically on each
    # syncdb/migrate for apps with migrations, hence the need to load them manually.
    # But it's a good thing because initial_data won't be overridden
    # each time syncdb/migrate is run (e.g. think of 'admin' user that
    # you manually changed password for).
    management.call_command('loaddata', "accounts_initial_data")


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data),
    ]
