#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import pkg_resources
import codecs
import fsaipe


with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    install_requires = [str(req) for req in pkg_resources.parse_requirements(f)]

setup(
    name='saipe',
    version=fsaipe.__version__,
    license="Apache",
    description='Flask SqlAlchemy In Place Editor',
    long_description=long_description,
    author='Gustavo vargas',
    author_email='xgvargas@gmail.com',
    url='https://github.com/xgvargas/saipe',
    # py_modules = ['saipe'],
    packages = ['fsaipe'],
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
