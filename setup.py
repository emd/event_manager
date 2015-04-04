try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'event_manager',
    'version': '0.1',
    'packages': ['event_manager'],
    'install_requires': ['numpy', 'matplotlib', 'nose'],
    'author': 'Evan M. Davis',
    'author_email': 'emd@mit.edu',
    'url': '',
    'description': 'Event management routines for Python.'
}

setup(**config)
