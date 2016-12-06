# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 13:12:11 2016

@author: ZengC
"""

from setuptools import setup

setup(
    name='tickets',
    py_modules=['tickets', 'stations'],
    install_requires=['requests', 'docopt', 'prettytable', 'colorama'],
    entry_points={
        'console_scripts': ['tickets=tickets:cli']
    }
)