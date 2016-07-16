# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


def create_site(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Site = apps.get_model('sites', 'Site')
    db_alias = schema_editor.connection.alias
    Site.objects.using(db_alias).create(
        pk=settings.SITE_ID,
        domain=settings.DOMAIN_NAME,
        name=settings.DOMAIN_NAME)


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_site),
    ]
