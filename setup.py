from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='pyNuvo',
      version=version,
      description="Nuvo Grand Concerto Communicator",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='nuvo concerto',
      author='Travis Bennett',
      author_email='tbennett81@hotmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
		'pyserial',
		'rpyc',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
