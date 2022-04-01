#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Manuel Holtgrewe",
    author_email='manuel.holtgrewe@bih-charite.de',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Slurm Text User Interface using the Slurm REST API in Python.",
    entry_points={
        'console_scripts': [
            'slurm_tui=slurm_tui.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='slurm_tui',
    name='slurm_tui',
    packages=find_packages(include=['slurm_tui', 'slurm_tui.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/holtgrewe/slurm_tui',
    version='0.1.0',
    zip_safe=False,
)
