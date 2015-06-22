# encoding: utf-8
# Copyright 2015 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from plone.dexterity.utils import createContentInContainer
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from ZODB.DemoStorage import DemoStorage
import pkg_resources, csv, logging, transaction

_logger = logging.getLogger(__name__)


def publish(item, wfTool=None):
    if wfTool is None:
        wfTool = getToolByName(item, 'portal_workflow')
    try:
        wfTool.doActionFor(item, action='publish')
        item.reindexObject()
    except WorkflowException:
        pass
    for i in item.objectIds():
        _logger.info('Getting child %s of item %s', i, item.id)
        subItem = item[i]
        publish(subItem, wfTool)


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
            _logger.info('Creating probeset %s', probesetID)
            createContentInContainer(
                secretome,
                'eke.secretome.probeset',
                title=probesetID,
                hgncSymbol=hgnc,
                databaseNames=databases,
                timesMapped=timesMapped
            )
    transaction.commit()
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
            _logger.info('Creating gene/protein %s', gene)
            createContentInContainer(
                secretome,
                'eke.secretome.geneprotein',
                title=gene,
                databaseNames=list(mapping.databases),
                probesetMappings=list(mapping.probesets)
            )
    transaction.commit()
    _logger.info('Publishing everything')
    publish(resources)
    transaction.commit()


def setupImportSteps(context):
    if context.readDataFile('eke.secretome.flag.txt') is None: return
    portal = context.getSite()
    loadSecretome(portal)
