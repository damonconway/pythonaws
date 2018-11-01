# -*- coding: utf-8 -*-

"""Create a webotron package."""

from setuptools import setup

setup(
    name='webotron-80',
    version='0.1',
    author='Damon Conway',
    author_email='damon@autopod.co',
    description='Webotron 80 is a tool to deploy static websites to AWS.',
    license='GPLv3+',
    packages=['webotron'],
    url='https://github.com/damonconway/pythonaws',
    install_requires=[
        'boto3',
        'click'
    ],
    entry_points='''
      [console_scripts]
      webotron=webotron.webotron:cli
    '''
)
