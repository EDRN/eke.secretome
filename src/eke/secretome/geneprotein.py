# encoding: utf-8
# Copyright 2015 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from eke.secretome import MESSAGE_FACTORY as _
from five import grok
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from zope import schema
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


class IGeneProtein(model.Schema):
    u'''A gene or a protein.'''
    title = schema.TextLine(
        title=_(u'Gene/Protein ID'),
        description=_(u'The identifier of this gene or protein.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this gene or protein.'),
        required=False,
    )
    databaseNames = schema.List(
        title=_(u'Database Names'),
        description=_(u'Names of the databases in which this gene/protein appears.'),
        required=True,
        unique=True,
        value_type=schema.TextLine(
            title=_(u'Database Name'),
            description=_(u'Name of a single database in which this gene/protein appears.')
        )
    )
    probesetMappings = schema.List(
        title=_(u'Mappings'),
        description=_(u'Affymetrix HGU133plus2 probeset mappings.'),
        required=False,
        value_type=schema.TextLine(
            title=_(u'Mappings'),
            description=_(u'Affymetrix HGU133plus2 probeset mapping.')
        )
    )


class DatabaseNamesVocabulary(object):
    u'''A vocabulary of names of databases'''
    grok.implements(IVocabularyFactory)
    def __call__(self, context):
        catalog = getToolByName(context, 'portal_catalog')
        results = list(catalog.uniqueValuesFor('databaseNames'))
        results.sort()
        return SimpleVocabulary.fromItems([(i.decode('utf-8'), i.decode('utf-8')) for i in results])
grok.global_utility(DatabaseNamesVocabulary, name=u'eke.secretome.DatabaseNamesVocabulary', direct=False)
