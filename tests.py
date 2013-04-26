import ssmp
import msg


def main():

    # Get a transport for a Redis Message Queue
    transport = ssmp.Transport(ssmp.Transport.RQ, redis_connect_args=**kwargs)

    # Default to all messages not having an ID  (Default is True)
    transport = ssmp.Transport(ssmp.Transport.RQ, id=False)

    # Default to all messages to encoding with JSON (Default is 'msgpack')
    transport = ssmp.Transport(ssmp.Transport.RQ, fmt='json')

    # Default to all messages not having an ID  (Default is True)
    # AND Default to all messages to encoding with JSON (Default is 'msgpack')
    transport = ssmp.Transport(ssmp.Transport.RQ, id=False, fmt='json')


    transport = ssmp.Transport(ssmp.Transport.RQ, fmt='msgpack')
    # transport = ssmp.Transport(ssmp.Transport.RQ, fmt='json')
    # transport = ssmp.Transport(ssmp.Transport.RQ, fmt='yaml')
    # transport = ssmp.Transport(ssmp.Transport.RQ, fmt='pickle')

    transport.send("A short message", id=True, fmt='json')
    transport.send("A short message", id=False, fmt='yaml')
    transport.send("A short message", id=False, fmt='pickle')
# main()

if __name__ == '__main__':
    main()
