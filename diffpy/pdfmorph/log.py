#!/usr/bin/env python
##############################################################################
#
# diffpy.pdfmorph   by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2010 Trustees of the Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Pavol Juhas, Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

"""Configuration of loggers used in this package.

Logger instances:

plog -- logger instance for normal operation
"""

# module version
__id__ = "$Id: log.py 1613 2012-03-14 18:56:22Z juhas $"

import logging

# logging configuration
plog = logging.getLogger('diffpy.pdfmorph')


def setVerbosity(vb):
    '''Set verbosity of the pdfmorph logger.

    vb   -- integer or one of ('debug', 'info', 'warning', 'error') strings

    No return value.
    '''
    try:
        if type(vb) is str:
            level = int(getattr(logging, vb.upper(), vb))
        else:
            level = int(vb)
    except (TypeError, AttributeError):
        emsg = "invalid value of verbose %r" % vb
        raise ValueError(emsg)
    plog.setLevel(level)
    plog.info("log level set to %r", level)
    return

# End of file
