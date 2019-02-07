# -*- coding: utf-8 -*-

# Learn more: https://github.com/danliberato/Cloud-Broker/README

from setuptools import setup


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='cloud-broker',
    version='1.0',
    description='A (very) simplified Cloud Broker system.',
    long_description=readme,
    author='Daniel Liberato',
    author_email='me@kennethreitz.com',
    url='https://github.com/danliberato/Cloud-Broker',
    license=license
)
