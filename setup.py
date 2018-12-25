#!/usr/bin/env python
from setuptools import setup, find_packages
import django_pivot


def read_file(name):
    with open(name) as fd:
        return fd.read()

keywords = ['django', 'web', 'data', 'html']

setup(
    name='django-pivot2',
    version=django_pivot.__version__,
    description=django_pivot.__doc__,
    long_description=read_file('README.rst'),
    author=django_pivot.__author__,
    author_email=django_pivot.__email__,
    install_requires=read_file('requirements.txt'),
    license='BSD',
    url=django_pivot.__url__,
    keywords=keywords,
    packages=find_packages(exclude=[]),
    include_package_data=True,
    test_suite='runtests.test',
    tests_require=read_file('requirements-tests.txt'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
