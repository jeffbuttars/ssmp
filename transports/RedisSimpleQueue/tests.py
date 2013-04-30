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

import unittest2 as unittest

from redissimplequeue import RedisSimpleQueue
import msg


class TestRedisSimpleQueue(unittest.TestCase):

    def setUp(self):
        """todo: Docstring for setUp
        :return:
        :rtype:
        """
        self.rsq = RedisSimpleQueue(msg.version_objs.get())

        # Pump the Q
        self.msgs = []

        for m in ("A test message 1", "A test message 2",
                  "A test message 3", "A test message 4"):
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
#TestRedisSimpleQueue


def suite():

    quick = None
    # quick = unittest.TestSuite()
    # # quick.addTest(TestVerizonDeviceV3('test_get_device_list'))
    # # quick.addTest(TestVerizonDeviceV3('test_get_device_detail'))
    # #quick.addTest(TestVerizonDeviceV3('test_delete_detail'))
    # # quick.addTest(TestVerizonDeviceV3('test_post_list'))
    # quick.addTest(TestVerizonDeviceListV5())

    suite_rsq = quick or \
        unittest.TestLoader().loadTestsFromTestCase(TestRedisSimpleQueue)

    return unittest.TestSuite([
        suite_rsq,
    ])
#suite()

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
