import logging
logger = logging.getLogger("ssmp")
import redis


class RedisSimpleQueue(object):

    def __init__(self, msg_type, redis_cfg=None, default_q='default_q'):
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

        logger.debug("redis_cfg: %s, default_q: %s", redis_cfg, default_q)

        self._redis_cfg = redis_cfg
        self._default_q = default_q
        self._conn = None
        self._msg_type = msg_type

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

        m = self._msg_type(msg)

        logger.debug("msg: %s, q:%s", m.msg, q)
        rq = q or self._default_q
        return self._conn.lpush(rq, m.msg) and m
    #push()

    def pop(self, q=None, num=None, cb=None):
        """todo: Docstring for recv

        :param cb: arg description
        :type cb: type description
        :return:
        :rtype:
        """
        logger.debug("q:%s, num:%s, cb:%s", q, num, cb)

        rq = q or self._default_q
        res = None

        # Return the whole Q
        if num == '-1':
            p = self._conn.pipeline()
            p.multi()
            p.lrange(rq, 0, -1)
            p.ltrim(rq, num, -1)
            res = p.execute()
            logger.debug("result: %s", res)
            return res

        # return at most num items
        if num:
            num = int(num)
            p = self._conn.pipeline()
            p.multi()
            p.lrange(rq, 0, num - 1)
            p.ltrim(rq, num, -1)
            res = p.execute()
            logger.debug("result: %s", res)
            return res

        # return the last item

        res = self._conn.lpop(rq)
        logger.debug("result: %s", res)
        res = self._msg_type.decode(res)
        logger.debug("result decoded: %s", res)

        return res
    #pop()
#RedisSimpleQueue
