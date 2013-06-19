

class RedisTest(object):

    def __init__(self, *args, **kwargs):
        """todo: to be defined

        :param *args: arg description
        :type *args: type description
        :param **kwargs: arg description
        :type **kwargs: type description
        """
        self._args = args
        self._kwargs = kwargs
        self._queues = {}
        self._trans = None
    #__init__()

    def __repr__(self):
        return "RedisTest server\nargs: {}\nkwargs: {}".format(
            self._args, self._kwargs)
    #__repr__()

    def _mq(self, q):
        if q not in self._queues:
            self._queues[q] = []

        return self._queues[q]
    #_mq()

    def lpush(self, q, msg):
        mq = self._mq(q)
        mq.insert(0, msg)
        return self
    #lpush()

    def lpop(self, q):
        mq = self._mq(q)
        mq.pop(0)
        return self
    #lpop()

    def pipline(self):
        return self
    #pipline()

    def multi(self):
        self._trans = []
    #multi()

    def lrange(self, q, b, e):
        """todo: Docstring for lrange

        :param q: arg description
        :type q: type description
        :param b: arg description
        :type b: type description
        :param e: arg description
        :type e: type description
        :return:
        :rtype:
        """

        mq = self._mq(q)
        return mq[b:e]
    #lrange()

    def ltrim(self, q, b, e):
        self._mq(q)
        self._queues[q] = self.lrange(q, b, e)
    #ltrim()

    def llen(self, q):
        """todo: Docstring for llen

        :param q: arg description
        :type q: type description
        :return:
        :rtype:
        """
        self._mq(q)
        return len(self._queues[q])
    #llen()

    def execute(self):
        """todo: Docstring for execute
        :return:
        :rtype:
        """
        pass
    #execute()
#RedisTest
