#!/usr/bin/env python
from setuptools import setup, find_packages

exec( open( 'pynuvo/package_version.py' ).read() )

setup(
    name = 'pyNuvo',
    version = __version__,
    packages=find_packages(),
    package_data = {
        'pynuvo': [
            'www/static/*.*',
            'www/static/css/smoothness/*.css',
            'www/static/css/smoothness/images/*.*',
            'www/static/js/*.js',
            'www/templates/admin/*.html',
            'www/templates/devdocs/jquery/*.html',
            ],
        },
    scripts = [
        'scripts/*.py'
        ],
    install_requires=[
        'pyserial>=2.7',
        'rpyc>=3.2.3',
        'django>=1.6.1'
    ],
    
    description="Nuvo Grand Concerto Communicator",
    author='Travis Bennett',
    author_email='tbennett81@hotmail.com',
)