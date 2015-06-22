# encoding: utf-8
# Copyright 2015 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

u'''Secretome for EKE — functional doctests.'''

import doctest
import unittest2 as unittest
from plone.testing import layered
from eke.secretome.testing import EKE_SECRETOME_FUNCTIONAL_TESTING as LAYER

optionFlags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE)


def test_suite():
    return unittest.TestSuite([
        layered(doctest.DocFileSuite('README.rst', package='eke.secretome', optionflags=optionFlags), LAYER),
    ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
