import logging
logger = logging.getLogger("ssmp")

from ssmp.transports import RedisBasicQueue


class RedisEndpointQueue(RedisBasicQueue):
    def __init__(self, **kwargs):
        """todo: to be defined """
        kwargs = kwargs or {}
        kwargs['msg_cls'] = 'endpoint'
        super(RedisEndpointQueue, self).__init__(**kwargs)
    #__init__()

    def push(self, ep, payload=None, q=None):
        """todo: Docstring for send
        """

        logger.debug("ep: %s, payload: %s, q:%s", ep, payload, q)

        logger.debug(self._msg_cls)
        m = self._msg_cls(ep, payload)

        rq = q or self._default_q
        return self._conn.lpush(rq, m.msg) and m
    #push()

#RedisEndpointQueue
