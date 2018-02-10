"""
SQLXerion
-------------
SQLAlchemy for humans
"""
import io
import re

from setuptools import setup

with io.open('xerion/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='SQLXerion',
    version=version,
    url='https://github.com/poteralski/sqlxerion',
    license='BSD',
    author='Piotr Poteralski',
    author_email='poteralski.dev@gmail.com',
    description='SQLAlchemy for humans',
    long_description=__doc__,
    packages=['xerion'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['SQLAlchemy'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)