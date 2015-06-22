This package provides representation of the Secretome within the EDRN_ portal.

To demonstrate how it works, we'll do a series of functional tests.  And to do
so, we'll need a test browser::

    >>> app = layer['app']
    >>> from plone.testing.z2 import Browser
    >>> from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
    >>> browser = Browser(app)
    >>> browser.handleErrors = False
    >>> browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
    >>> portal = layer['portal']    
    >>> portalURL = portal.absolute_url()

Here we go.


Secretome Folders
=================

Secretome Folders are used to contain Secretome entries.  They may be created
anywhere::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='eke-secretome-secretomefolder')
    >>> l.url.endswith('++add++eke.secretome.secretomefolder')
    True
    >>> l.click()
    >>> browser.getControl(name='form.widgets.title').value = u'Sticky Secretions'
    >>> browser.getControl(name='form.widgets.description').value = u'Where I keep my sticky substances.'
    >>> browser.getControl(name='form.buttons.save').click()
    >>> 'sticky-secretions' in portal.keys()
    True
    >>> folder = portal['sticky-secretions']
    >>> folder.title
    u'Sticky Secretions'
    >>> folder.description
    u'Where I keep my sticky substances.'


Genes and Proteins
==================

Genes and proteins go into Secretome Folders::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='eke-secretome-geneprotein')
    Traceback (most recent call last):
    ...
    LinkNotFoundError
    >>> browser.open(portalURL + '/sticky-secretions')
    >>> l = browser.getLink(id='eke-secretome-geneprotein')
    >>> l.url.endswith('++add++eke.secretome.geneprotein')
    True
    >>> l.click()
    >>> browser.getControl(name='form.widgets.title').value = u'Snot.123456'
    >>> browser.getControl(name='form.widgets.description').value = u'Got this secretion out of my nose.'
    >>> browser.getControl(name='form.widgets.databaseNames').value = u'SnotDB-1\nSticky in Stanford'
    >>> browser.getControl(name='form.widgets.probesetMappings').value = u'1234_ab\n5678_cd'
    >>> browser.getControl(name='form.buttons.save').click()
    >>> 'snot-123456' in folder.keys()
    True
    >>> gene = folder['snot-123456']
    >>> gene.title
    u'Snot.123456'
    >>> gene.description
    u'Got this secretion out of my nose.'
    >>> gene.databaseNames
    [u'SnotDB-1', u'Sticky in Stanford']
    >>> gene.probesetMappings
    [u'1234_ab', u'5678_cd']

Works great.  Note the database names are required::

    >>> browser.open(portalURL + '/sticky-secretions')
    >>> browser.getLink(id='eke-secretome-geneprotein').click()
    >>> browser.getControl(name='form.widgets.title').value = u'Snot.34567'
    >>> browser.getControl(name='form.buttons.save').click()
    >>> browser.contents
    '...Required input is missing...'


Probesets
=========

Affymetrix HGU133plus2 probesets are what genes or proteins are mapped to.  They
too only go into Secretome Folders::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='eke-secretome-probeset')
    Traceback (most recent call last):
    ...
    LinkNotFoundError
    >>> browser.open(portalURL + '/sticky-secretions')
    >>> l = browser.getLink(id='eke-secretome-probeset')
    >>> l.url.endswith('++add++eke.secretome.probeset')
    True
    >>> l.click()
    >>> browser.getControl(name='form.widgets.title').value = u'207559_snot'
    >>> browser.getControl(name='form.widgets.description').value = u'Got this secretion out of my other nose.'
    >>> browser.getControl(name='form.widgets.hgncSymbol').value = u'QVC-CVS'
    >>> browser.getControl(name='form.widgets.databaseNames').value = u'SnotDB-1\nSticky in Stanford'
    >>> browser.getControl(name='form.widgets.timesMapped').value = u'12'
    >>> browser.getControl(name='form.buttons.save').click()
    >>> '207559_snot' in folder.keys()
    True
    >>> probeset = folder['207559_snot']
    >>> probeset.title
    u'207559_snot'
    >>> probeset.description
    u'Got this secretion out of my other nose.'
    >>> probeset.hgncSymbol
    u'QVC-CVS'
    >>> probeset.databaseNames
    [u'SnotDB-1', u'Sticky in Stanford']
    >>> probeset.timesMapped
    12

Looks good.

.. References:
.. _EDRN: http://edrn.nci.nih.gov/
