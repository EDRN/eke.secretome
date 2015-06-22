# encoding: utf-8
# Copyright 2015 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.layout.interfaces import IFacetedLayout
from eea.facetednavigation.settings.interfaces import IHidePloneLeftColumn, IHidePloneRightColumn
from eke.secretome import MESSAGE_FACTORY as _
from five import grok
from geneprotein import IGeneProtein
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from zope import schema
from zope.component import getMultiAdapter
from zope.interface import noLongerProvides
from zope.lifecycleevent.interfaces import IObjectAddedEvent


class ISecretomeFolder(model.Schema):
    u'''A folder containing secretomic information.'''
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'The name of this folder'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this folder.'),
        required=False,
    )


@grok.subscribe(ISecretomeFolder, IObjectAddedEvent)
def installFacetedNavigation(obj, event):
    if not ISecretomeFolder.providedBy(obj): return
    factory = getToolByName(obj, 'portal_factory')
    if factory.isTemporary(obj): return
    request = obj.REQUEST
    subtyper = getMultiAdapter((obj, request), name=u'faceted_subtyper')
    if subtyper.is_faceted or not subtyper.can_enable: return
    subtyper.enable()
    criteria = ICriteria(obj)
    for cid in criteria.keys():
        criteria.delete(cid)
    criteria.add('resultsperpage', 'bottom', 'default', title='Results per page', hidden=True, start=0, end=50, step=5,
        default=20)
    criteria.add(
        'checkbox', 'bottom', 'default',
        title='Obj provides',
        hidden=True,
        index='object_provides',
        operator='or',
        vocabulary=u'eea.faceted.vocabularies.ObjectProvides',
        default=[IGeneProtein.__identifier__],
        count=False,
        maxitems=0,
        sortreversed=False,
        hidezerocount=False
    )
    criteria.add('debug', 'top', 'default', title='Debug Criteria', user='kelly')
    criteria.add(
        'checkbox', 'left', 'default',
        title=u'Databases',
        hidden=False,
        index='databaseNames',
        operator='or',
        vocabulary=u'eke.secretome.DatabaseNamesVocabulary',
        count=False,
        maxitems=0,
        sortreversed=False,
        hidezerocount=False
    )
    IFacetedLayout(obj).update_layout(u'faceted_secretome_view')
    noLongerProvides(obj, IHidePloneLeftColumn)
