from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='crowdsource',
    version='0.1.0',
    description='Realtime Competitions',
    long_description=long_description,
    url='https://github.com/timkpaine/crowdsource',
    download_url='https://github.com/timkpaine/crowdsource/archive/v0.1.0.tar.gz',
    author='Tim Paine',
    author_email='timothy.k.paine@gmail.com',
    license='Apache 2.0',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='realtime competition streaming',
    zip_safe=False,
    packages=find_packages(exclude=[]),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'server=crowdsource.server:main',
            'client=crowdsource.client:main',
        ],
    },
)
