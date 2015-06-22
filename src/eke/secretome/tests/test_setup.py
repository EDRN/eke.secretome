# encoding: utf-8
#
# Copyright 2015 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

u'''Secretome for EKE — setup tests'''

from eke.secretome.testing import EKE_SECRETOME_INTEGRATION_TESTING
from Products.CMFCore.utils import getToolByName
import unittest2 as unittest

class SetupTest(unittest.TestCase):
    layer = EKE_SECRETOME_INTEGRATION_TESTING
    def setUp(self):
        super(SetupTest, self).setUp()
        self.portal = self.layer['portal']
    def testTypes(self):
        u'''Check types'''
        types = getToolByName(self.portal, 'portal_types')
        for t in ('eke.secretome.secretomefolder',):
            self.failUnless(t in types, u'Type {} not in portal_types'.format(t))
        # folderType = types['eke.secretome.secretomefolder']
        # self.failUnless('eke.secretome.secretomedataset' in folderType.allowed_content_types,
        #     u"eke.secretome.secretomedataset doesn't appear in eke.secretome.labcasfolder's allowed types")
    def testCatalog(self):
        u'''Ensure catalog indexes and schemata are installed'''
        catalog = getToolByName(self.portal, 'portal_catalog')
        indexes = catalog.indexes()
        for index in ('databaseNames', 'probesetMappings'):
            self.failUnless(index in indexes, 'Expected index "{}" in catalog'.format(index))
        schema = catalog.schema()
        for index in ('databaseNames', 'probesetMappings'):
            self.failUnless(index in schema, 'Expected index "{}" in catalog schema'.format(index))
