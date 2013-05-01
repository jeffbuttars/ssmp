#!/usr/bin/env python
# encoding: utf-8

import logging
logger = logging.getLogger('ssmp')


from msgbase import find_codec
from msg_basic import Msg as BasicMsg


class Msg(BasicMsg):
    def __init__(self, endpoint, payload, *args, **kwargs):
        """todo: to be defined """
        self._ver = 2
        super(Msg, self).__init__(payload, *args, **kwargs)

        self._ep = endpoint
    #__init__()

    @property
    def endpoint(self):
        return self._ep
    #endpoint()

    @endpoint.setter
    def property(self, data, delay=False):
        self._ep = data
        if not delay:
            self._msg = self.serialized
    #property()

    @classmethod
    def decode(cls, msg):
        logger.debug("msg: %s", msg)

        parts = msg.split(':', 4)
        fmt = parts[2]
        codec = find_codec(fmt)
        return cls(parts[3], codec.decode(parts[4]), id=parts[1], fmt=fmt)
    #decode()

    @property
    def serialized(self):
        return "{}:{}:{}:{}:{}".format(self._ver, self._id,
                                       self._fmt, self._ep,
                                       self._codec.encode(self._payload))
    #serialized()
#Msg
