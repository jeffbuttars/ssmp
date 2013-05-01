#!/usr/bin/env python
# encoding: utf-8

import logging
logger = logging.getLogger('ssmp')


from msgbase import find_codec
import msg_basic


class Msg(msg_basic.Msg):
    def __init__(self, endpoint, payload=None, *args, **kwargs):
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
    def endpoint(self, data, delay=False):
        self._ep = data
        if not delay:
            self._msg = self.serialized
    #endpoint()

    @classmethod
    def decode(cls, msg):
        logger.debug("msg: %s", msg)

        parts = msg.split(':', 4)
        fmt = parts[2]
        codec = find_codec(fmt)
        pl = parts[4]
        pl = pl and codec.decode(pl)
        return cls(parts[3], pl, id=parts[1], fmt=fmt)
    #decode()

    @property
    def serialized(self):
        # The payload can be empty! A quick and cheesy way to
        # fire events.
        pl = self._payload and self._codec.encode(self._payload)

        return "{}:{}:{}:{}:{}".format(self._ver, self._id,
                                       self._fmt, self._ep,
                                       pl)
    #serialized()
#Msg
