from __future__ import absolute_import
import logging

from django.shortcuts import render


logger = logging.getLogger(__name__)


def homepage(request, template='marketing/homepage.html'):
    """Returns homepage.html for the root url"""
    logger.info('this homepage rocks!!!')
    return render(request, template, {})


def examples(request, template='marketing/examples.html'):
    """Returns homepage.html for the root url"""
    return render(request, template, {})
