#!/usr/bin/env python
# encoding: utf-8

"""
Uceem Networks Incorporated. Confidential
--------------------------------

© Copyright 2012 - 2013 Uceem Networks.
All Rights Reserved.

NOTICE: All information contained herein is, and remains
the property of Uceem Networks Incorporated and its suppliers,
if any.  The intellectual and technical concepts contained
herein are proprietary to Uceem Networks Incorporated
and its suppliers and may be covered by U.S. and Foreign Patents,
patents in process, and are protected by trade secret or copyright law.
Dissemination of this information or reproduction of this material
is strictly forbidden unless prior written permission is obtained
from Uceem Networks Incorporated.
"""

import logging
logger = logging.getLogger('ssmp')
import sys
sys.path.append('../..')
import datetime

import unittest2 as unittest

from redissimplequeue import RedisBasicQueue


class TestRedisBasicQueue(unittest.TestCase):

    def setUp(self):
        """todo: Docstring for setUp
        :return:
        :rtype:
        """
        self.rsq = RedisBasicQueue(default_q='rsq_test_q')
        self.rsq.remove()

        # Pump the Q
        self.msgs = []

        for m in ("A test message 1", "A test message 2",
                  "A test message 3", {'foo': "A test message 4",
                                       'bar': "blafdjafjds",
                                       'now': datetime.datetime.now()}):
            self.msgs.append(self.rsq.push(m))
        # end for m in msgs
    #setUp()

    def test_one_item(self):
        """todo: Docstring for test_one_item
        :return:
        :rtype:
        """

        res = self.rsq.pop()
        exp = self.msgs.pop()

        self.assertEqual(res.ver, exp.ver)
        self.assertEqual(res.id, exp.id)
        self.assertEqual(res.fmt, exp.fmt)
        self.assertEqual(res.payload, exp.payload)
    #test_one_item()

    def test_all_items(self):
        for item in self.rsq.pops():
            print(item)
    #test_all_items()

    def test_some_items(self):
        for item in self.rsq.pops(num=2):
            print(item)
    #test_some_items()
#TestRedisBasicQueue


def suite():

    quick = None
    # quick = unittest.TestSuite()
    # # quick.addTest(TestVerizonDeviceV3('test_get_device_list'))
    # # quick.addTest(TestVerizonDeviceV3('test_get_device_detail'))
    # #quick.addTest(TestVerizonDeviceV3('test_delete_detail'))
    # # quick.addTest(TestVerizonDeviceV3('test_post_list'))
    # quick.addTest(TestVerizonDeviceListV5())

    suite_rsq = quick or \
        unittest.TestLoader().loadTestsFromTestCase(TestRedisBasicQueue)

    return unittest.TestSuite([
        suite_rsq,
    ])
#suite()

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
