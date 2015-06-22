# encoding: utf-8
# Copyright 2015 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from plone.app.testing import PloneSandboxLayer, IntegrationTesting, FunctionalTesting, PLONE_FIXTURE
from Products.CMFCore.utils import getToolByName
from eke.secretome import PACKAGE_NAME
import pkg_resources, urllib2, urllib, httplib


class EKESecretomeLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        import eke.secretome
        self.loadZCML(package=eke.secretome)
    def setUpPloneSite(self, portal):
        wfTool = getToolByName(portal, 'portal_workflow')
        wfTool.setDefaultChain('plone_workflow')
        self.applyProfile(portal, 'eke.secretome:default')


EKE_SECRETOME = EKESecretomeLayer()

EKE_SECRETOME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EKE_SECRETOME,),
    name='EKESecretomeLayer:Integration'
)

EKE_SECRETOME_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EKE_SECRETOME,),
    name='EKESecretomeLayer:Functional'
)
