# encoding: utf-8
# Copyright 2015 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from plone.dexterity.utils import createContentInContainer
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from ZODB.DemoStorage import DemoStorage
import pkg_resources, csv


def publish(item, wfTool=None):
    if wfTool is None:
        wfTool = getToolByName(item, 'portal_workflow')
    try:
        wfTool.doActionFor(item, action='publish')
        item.reindexObject()
    except WorkflowException:
        pass
    for i in item.keys():
        try:
            subItem = item[i]
            publish(subItem, wfTool)
        except AttributeError:
            pass


def loadSecretome(portal):
    if portal._p_jar is not None and isinstance(portal._p_jar.db()._storage, DemoStorage):
        # Don't bother if we're just testing
        return
    try:
        resources = portal['resources']
    except KeyError:
        resources = portal[portal.invokeFactory('Folder', 'resrouces')]
        resources.title = u'Resources'
    try:
        secretome = resources['secretome']
    except KeyError:
        secretome = createContentInContainer(resources, 'eke.secretome.secretomefolder', title=u'Secretome')
    ids = secretome.keys()
    if len(ids) > 0:
        secretome.manage_delObjects(list(ids))
    with pkg_resources.resource_stream(__name__, 'data/uniqueIDs.csv') as infile:
        rows = csv.DictReader(infile)
        for row in rows:
            probesetID, hgnc, timesMapped = row['hgu133plus2ID'], row['HGNC.symbol'], int(row['times.mapped.to'])
            databases = row['databases.foundin'].split(u'|')
            createContentInContainer(
                secretome,
                'eke.secretome.probeset',
                title=probesetID,
                hgncSymbol=hgnc,
                databaseNames=databases,
                timesMapped=timesMapped
            )
    with pkg_resources.resource_stream(__name__, 'data/mappedIDs.csv') as infile:
        rows = csv.DictReader(infile)
        mappings = {}
        class Mapping(object):
            def __init__(self):
                self.databases, self.probesets = set(), set()
        for row in rows:
            database, gene, probesets = row['database'], row['beforemapping'], row['hgu133plus2.ID']
            if probesets == 'none':
                probesets = set()
            else:
                probesets = set(probesets.split(u'|'))
            mapping = mappings.get(gene, Mapping())
            mapping.databases.add(database)
            mapping.probesets = mapping.probesets | probesets
            mappings[gene] = mapping
        for gene, mapping in mappings.iteritems():
            createContentInContainer(
                secretome,
                'eke.secretome.geneprotein',
                title=gene,
                databaseNames=list(mapping.databases),
                probesetMappings=list(mapping.probesets)
            )
    publish(resources)


def setupImportSteps(context):
    if context.readDataFile('eke.secretome.flag.txt') is None: return
    portal = context.getSite()
    loadSecretome(portal)
