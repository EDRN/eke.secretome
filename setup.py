# encoding: utf-8
# Copyright 2015 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from setuptools import setup, find_packages
from ConfigParser import SafeConfigParser
import os.path

# Package data
# ------------

_name            = 'eke.secretome'
_version         = '0.0.0'
_description     = 'Secreted molecules and elements by cells, tissues, organs, and organisms'
_author          = 'Sean Kelly'
_authorEmail     = 'sean.kelly@jpl.nasa.gov'
_maintainer      = 'Sean Kelly'
_maintainerEmail = 'sean.kelly@jpl.nasa.gov'
_license         = 'ALv2'
_namespaces      = ['eke']
_zipSafe         = False
_keywords        = 'web zope plone edrn cancer biomarkers eke knowledge secretome secretions'
_testSuite       = 'eke.secretome.tests.test_suite'
_entryPoints     = {
    'z3c.autoinclude.plugin': ['target=plone'],
}
_extras = {
    'test': ['plone.app.testing'],
}
_externalRequirements = [
    'setuptools',
    'Products.CMFPlone',
    'z3c.autoinclude',
    'plone.app.dexterity[grok]',
    'eea.facetednavigation',
]
_classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Framework :: Plone',
    'Intended Audience :: Healthcare Industry',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

# Setup Metadata
# --------------

def _read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

_header = '*' * len(_name) + '\n' + _name + '\n' + '*' * len(_name)
_longDescription = _header + '\n\n' + _read('README.rst') + '\n\n' + _read('docs', 'INSTALL.txt') + '\n\n' \
    + _read('docs', 'HISTORY.txt') + '\n'
open('doc.txt', 'w').write(_longDescription)

setup(
    author=_author,
    author_email=_authorEmail,
    classifiers=_classifiers,
    description=_description,
    entry_points=_entryPoints,
    extras_require=_extras,
    include_package_data=True,
    install_requires=_externalRequirements,
    keywords=_keywords,
    license=_license,
    long_description=_longDescription,
    maintainer=_maintainer,
    maintainer_email=_maintainerEmail,
    name=_name,
    namespace_packages=_namespaces,
    packages=find_packages('src', exclude=['ez_setup', 'bootstrap']),
    package_dir={'': 'src'},
    url='https://github.com/EDRN/' + _name,
    version=_version,
    zip_safe=_zipSafe,
)
