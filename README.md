# SuperSimpleMessageProtocols
## Oh God, Why??

Have you looked at the source code for Celery? It's nice and easy to use, but
IMHO, it does job queuing in a brittle, and incorrect, way. Celery, and others
like it, ties your client code base(she who pushes the job/task) to the
Q consumer, (he who runs the job/task). They must be the same code base. I'm not
ok with that. Plus, it means my web app is also my application service, although
Celery somewhat hides that from you.
Personally, I want them to be separate, opaque, and hopefully simple units. My 
web app should only be concerned with the webby stuff, not the funky long running
processes I need to deal with.

## What is this?

### Msg

It's a simple message format(s), Msg, that is text based for easier introspection
and debugging of the messages. Each Msg also supports a payload that can, and
should, be serialized. By default Msg payloads are serialized using msgpack.

### Transport

A transport is an abstraction of a Msg type(there are many) and the underlying
network protocol, topology, arrangement(Queue, a channel, PUB/SUB, etc.).
For instance, my transport is a basic message, msg\_basic, Queue based on a Redis broker.

# Easy!

This is how to send a Msg to my basic Redis Q (Make sure you have a local Redis server runing):

    > rbq = ssmp.RedisBasicQueue()
    > msg = rbq.push({'foo': 'bar'})  # Any python data structure, supported by msgpack, will do here

The `push` method returns the Msg instance created and pushed by the transport.

On the receiving end:

    > rbq = ssmp.RedisBasicQueue()
    > msg = rbq.pop()
    > rbq.len()  # How many messages are in the Q?

    A simple pattern:
    > if rbq.len():
    >   msg = rbq.pop()
    >   while msg:
    >       <do stuff>
    >       msg = rbq.pop()

Access the Msg instance attributes directly:

    > id = msg.id
    > payload = msg.payload  # This has been de-serialized into Python for you already
    > trans = msg.transport  # get reference to the transport this came from

### Extendable

Adding new Msg types and transports should be easy.

# TODO:

* Tests! Oh my, no tests yet.
* Better cooler transports for ZMQ and Tornado for some great true eventing from
a web app to a Tornado application service consumer.
