##############################################################################
#
# diffpy.pdfmorph   by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2010 Trustees of the Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################


"""class MorphSmear -- smear the objective.
"""

# module version
__id__ = "$Id$"


import numpy
from diffpy.pdfmorph.morphs.morph import *

class MorphSmear(Morph):
    '''Smear the objective function.

    This smears (broadens) the peaks of the objective.  Note that this operates
    on the RDF. Inputs are not automatically converted to the RDF.

    Attributes:

    sigma   --  The smear factor to apply to yrefin.

    '''

    # Define input output types
    summary = 'Scale objective by desired amount or to the reference'
    xinlabel = LABEL_RA
    yinlabel = LABEL_RR
    xoutlabel = LABEL_RA
    youtlabel = LABEL_RR

    def morph(self, xobj, yobj, xref, yref):
        """Resample arrays onto specified grid."""
        Morph.morph(self, xobj, yobj, xref, yref)
        self._smear(self.sigma)
        return self.xyallout

    def _smear(self, sigma):
        """Smear the peaks by the smear factor."""

        if sigma == 0: return

        # The Gaussian to convolute with. No need to normalize, we'll do that
        # later.
        r = self.xobjin
        rr = self.yobjin
        r0 = r[len(r) / 2]
        gaussian = numpy.exp(-0.5 * ((r - r0)/sigma)**2 ) 

        # Get the full convolution
        c = numpy.convolve(rr, gaussian, mode="full")
        # Find the centroid of the RDF, we don't want this to change from the
        # convolution.
        x1 = numpy.arange(len(rr), dtype=float)
        c1idx = numpy.sum(rr * x1)/sum(rr)
        # Find the centroid of the convolution
        xc = numpy.arange(len(c), dtype=float)
        ccidx = numpy.sum(c * xc)/sum(c)
        # Interpolate the convolution such that the centroids line up. This
        # uses linear interpolation.
        shift = ccidx - c1idx
        x1 += shift
        rrbroad = numpy.interp(x1, xc, c)

        # Normalize so that the integrated magnitude of the RDF doesn't change.
        rrbroad /= sum(gaussian)

        self.yobjout = rrbroad

        return

# End of class MorphSmear
