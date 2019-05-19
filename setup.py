#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages

setup(
    name='bilderfee',
    version='0.1.0',
    description='Django/Jinja2 Templatetags Bilderfee.',
    url='https://developer.bilder-fee.de/',
    author='Bilderfee',
    author_email='hello@bilderfee.de',
    platforms=['OS Independent'],
    include_package_data=True,
    packages=find_packages(),
    tests_require=[
        'enum34',
        'pytest',
        'pytest-cov',
        'pytest-django',
        'pytest-mock'
    ],
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Severside',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: MIT',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Multimedia :: Image',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
