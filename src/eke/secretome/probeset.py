# encoding: utf-8
# Copyright 2015 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from eke.secretome import MESSAGE_FACTORY as _
from plone.supermodel import model
from zope import schema


class IProbeset(model.Schema):
    u'''An Affymetrix HGU133plus2 Probeset ID.'''
    title = schema.TextLine(
        title=_(u'Probeset ID'),
        description=_(u'The probest identifier of this array.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this probeset.'),
        required=False,
    )
    hgncSymbol = schema.TextLine(
        title=_(u'HGNC Symbol'),
        description=_(u'HUGO Gene Nomenclature Committee identifier.'),
        required=True,
    )
    databaseNames = schema.List(
        title=_(u'Database Names'),
        description=_(u'Names of the databases from which this probeset is mapped.'),
        required=True,
        unique=True,
        value_type=schema.TextLine(
            title=_(u'Database Name'),
            description=_(u'Name of a single database from which this probeset is mapped.')
        )
    )
    timesMapped = schema.Int(
        title=_(u'Times Mapped'),
        description=_(u'The number of original identifiers in any secreted protein database that mapped to this identifier.'),
        required=True,
        min=0
    )
