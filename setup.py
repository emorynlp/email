# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='email-mining',
    version='0.1.0',
    description='Convert raw enron email data set to json format.',
    long_description=readme,
    author='Gary Lai',
    author_email='gary.lai@emory.edu',
    url='https://github.com/emorynlp/email-mining',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)