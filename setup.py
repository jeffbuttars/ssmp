#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

setup(name="ssmp",
      version='0.5',
      description="Super Simple Message Protocol",
      author="Jeff Buttars",
      author_email="jeffbuttars@gmail.com",
      packages=['ssmp', 'ssmp.transports', 'ssmp.msgs',
                'ssmp.transports.RedisSimpleQueue'
                ],
      install_requires=['PyYaml',
                        'python-msgpack',
                        'unittest2',
                        'redis',
                        'dateutil']
      )
