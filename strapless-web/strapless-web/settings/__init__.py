from __future__ import absolute_import
import os

# import defaults
from .base import *


overrides = __import__(
    ENV,
    globals(),
    locals(),
    ['settings']
)

# apply imported overrides
for attr in dir(overrides):
    # we only want to import settings (which have to be variables in ALLCAPS)
    if attr.isupper():
        # update our scope with the imported variables. We use globals() instead of locals()
        # because locals() is readonly and it returns a copy of itself upon assignment.
        globals()[attr] = getattr(overrides, attr)
