"""
SQLXerion
-------------
Legendary SQL-alchemical code capable of turning your code into gold
"""
from setuptools import setup


setup(
    name='SQLXerion',
    version='0.0.1',
    url='https://github.com/rstit/sqlxerion',
    license='BSD',
    author='Piotr Poteralski',
    author_email='poteralski.dev@gmail.com',
    description='Segendary SQL-alchemical code capable of turning your code into gold',
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