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
    url='https://github.com/rstit/flask-image-alchemy',
    license='BSD',
    author='RST-IT',
    author_email='piotr.poteralski@rst-it.com',
    description='SQLAlchemy Standarized Image Field for Flask',
    long_description=__doc__,
    packages=['flask_image_alchemy', 'flask_image_alchemy.storages'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['SQLAlchemy', 'wand', 'boto3'],
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