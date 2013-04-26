#!/usr/bin/env python
# encoding: utf-8
"""
    SSMP Msg version 1
"""

import msgbase


class Msg(msgbase.MsgBase):
    def __init__(self, *args, **kwargs):
        """todo: to be defined """
        self._ver = 1
        super(Msg, self).__init__(args, kwargs)
    #__init__()
#Msg
