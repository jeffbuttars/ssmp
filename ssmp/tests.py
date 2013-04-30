#!/usr/bin/env python
# encoding: utf-8

import logging

# Set up the logger
logger = logging.getLogger('ssmp')
# Use a console handler, set it to debug by default
logger_ch = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter(('%(asctime)s %(levelname)s:%(process)s'
                                   ' %(lineno)s:%(module)s:%(funcName)s()'
                                   ' %(message)s'))
logger_ch.setFormatter(log_formatter)
logger.addHandler(logger_ch)

# import msg
from transports import RedisSimpleQueue as RSQ


def main():

    # # Get a transport for a Redis Message Queue
    # transport = ssmp.Transport(ssmp.Transport.RQ, redis_connect_args=**kwargs)

    # # Default to all messages not having an ID  (Default is True)
    # transport = ssmp.Transport(ssmp.Transport.RQ, id=False)

    # # Default to all messages to encoding with JSON (Default is 'msgpack')
    # transport = ssmp.Transport(ssmp.Transport.RQ, fmt='json')

    # # Default to all messages not having an ID  (Default is True)
    # # AND Default to all messages to encoding with JSON (Default is 'msgpack')
    # transport = ssmp.Transport(ssmp.Transport.RQ, id=False, fmt='json')


    # transport = ssmp.Transport(ssmp.Transport.RQ, fmt='msgpack')
    # # transport = ssmp.Transport(ssmp.Transport.RQ, fmt='json')
    # # transport = ssmp.Transport(ssmp.Transport.RQ, fmt='yaml')
    # # transport = ssmp.Transport(ssmp.Transport.RQ, fmt='pickle')

    # transport.send("A short message", id=True, fmt='json')
    # transport.send("A short message", id=False, fmt='yaml')
    # transport.send("A short message", id=False, fmt='pickle')

    rsq = RSQ()
    rsq.push("A message")
    print(rsq.pop())
# main()

if __name__ == '__main__':
    main()
