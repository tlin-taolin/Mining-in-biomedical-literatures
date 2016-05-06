# -*- coding: utf-8 -*-
#
# Get fully qualified name for an object (including module and class names)
#

from settings.parameters import *


def get_fullname(o):
    return '%s.%s' % (o.__module__, o.__class__.__name__)
