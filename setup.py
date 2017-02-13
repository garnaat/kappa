#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kappa import __version__
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def open_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))


def run_setup():
    setup(
        name='kappa',
        version=__version__,
        description='A CLI tool for AWS Lambda developers',
        long_description=open_file('README.rst').read(),
        url='https://github.com/garnaat/kappa',
        author='Mitch Garnaat',
        author_email='mitch@garnaat.com',
        license='Apache License 2.0',
        packages=['kappa', 'kappa.scripts', 'kappa.event_source'],
        package_data={'kappa': ['_version']},
        package_dir={'kappa': 'kappa'},
        entry_points="""
            [console_scripts]
            kappa=kappa.scripts.cli:cli
        """,
        install_requires=open_file('requirements.txt').readlines(),
        test_suite='tests',
        include_package_data=True,
        zip_safe=True,
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'Natural Language :: English',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5'
        ],
    )

if __name__ == '__main__':
    run_setup()
