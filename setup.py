#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

setup(name="ssmp",
      version='0.6',
      description="Super Simple Message Protocol",
      author="Jeff Buttars",
      author_email="jeffbuttars@gmail.com",
      packages=['ssmp', 'ssmp.transports', 'ssmp.msgs',
                'ssmp.transports.RedisBasicQueue',
                'ssmp.transports.RedisEndpointQueue',
                ],
      install_requires=['PyYAML',
                        'msgpack-python',
                        'unittest2',
                        'redis',
                        'python-dateutil']
      )
