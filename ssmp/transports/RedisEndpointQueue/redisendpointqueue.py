from ssmp.transports import RedisBasicQueue


class RedisEndpointQueue(RedisBasicQueue):
    def __init__(self, msg_class='endpoint', **kwargs):
        """todo: to be defined """
        super(kwargs, self).__init__(msg_class, **kwargs)
    #__init__()
#RedisEndpointQueue
