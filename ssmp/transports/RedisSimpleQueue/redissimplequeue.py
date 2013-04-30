import logging
logger = logging.getLogger("ssmp")
import redis


from ssmp import msg

class RedisSimpleQueue(object):

    def __init__(self, msg_type=None, redis_cfg=None, default_q='default_q'):
        """
        redis_cfg = {
            conn: <Existing Redis connection>,
            host: <redis server hosthame>,
            port: <redis port>,
            db: <redis db number>
        }

        :param redis_cfg: arg description
        :type redis_cfg: type description
        """

        logger.debug("msg_type: %s, redis_cfg: %s, default_q: %s",
                     msg_type, redis_cfg, default_q)

        self._redis_cfg = redis_cfg
        self._default_q = default_q
        self._conn = None
        self._msg_type = msg_type or msg.version_objs.get()

        if self._redis_cfg:
            if 'conn' in self._redis_cfg:
                self._conn = self._redis_cfg['conn']
            else:
                self._conn = redis.Redis(**self._redis_cfg)

        if not self._conn:
            self._conn = redis.Redis()

        logger.debug("redis conn: %s", self._conn)
    #__init__()

    def push(self, msg, q=None):
        """todo: Docstring for send

        :param msg: arg description
        :type msg: type description
        :return:
        :rtype:
        """

        logger.debug("msg: %s, q:%s", msg, q)

        logger.debug(self._msg_type)
        m = self._msg_type(msg)

        rq = q or self._default_q
        return self._conn.lpush(rq, m.msg) and m
    #push()

    def pop(self, q=None):
        """todo: Docstring for recv

        :param cb: arg description
        :type cb: type description
        :return:
        :rtype:
        """
        logger.debug("q:%s", q)

        rq = q or self._default_q

        # return the last item
        res = self._conn.lpop(rq)
        logger.debug("result: %s", res)

        if res:
            res = self._msg_type.decode(res)
            logger.debug("result decoded: %s", res)

        return res
    #pop()

    def pops(self, q=None, num=None):
        # Pop a slice, a generator

        rq = q or self._default_q

        # Return the whole Q
        if not num:
            p = self._conn.pipeline()
            p.multi()
            p.lrange(rq, 0, -1)
            p.ltrim(rq, num, -1)
            res = p.execute()[0]
            logger.debug("result: %s", res)
            if res:
                while res:
                    yield self._msg_type.decode(res.pop())

        # return at most num items
        if num:
            num = int(num)
            p = self._conn.pipeline()
            p.multi()
            p.lrange(rq, 0, num - 1)
            p.ltrim(rq, num, -1)
            res = p.execute()[0]
            logger.debug("result: %s", res)
            if res:
                while res:
                    yield self._msg_type.decode(res.pop())
    #pops()

    def remove(self, q=None):
        rq = q or self._default_q
        return self._conn.ltrim(rq, 1, 0)
    #remove()
#RedisSimpleQueue
