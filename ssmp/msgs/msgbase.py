import logging
logger = logging.getLogger('ssmp')

from uuid import uuid4
import importlib
import datetime
import dateutil.parser

_CODEC_CACHE = {}


class CodecSubBase(object):
    """Docstring for CodecSubBase """

    def __init__(self, mod):
        """todo: to be defined """

        self._ser_cls = importlib.import_module(mod)
    #__init__()

    def decode(self, data):
        raise NotImplementedError("Subclasses must implement this.")
    #decode()

    def encode(self, data):
        raise NotImplementedError("Subclasses must implement this.")
    #encode()

    def _encode_datetime(self, obj):
        """datetime encoder
        Check it out: https://pypi.python.org/pypi/msgpack-python/

        :param obj: arg description
        :type obj: type description
        :return:
        :rtype:
        """
        if isinstance(obj, datetime.datetime):
            return {b'__datetime__': True, b'as_str': obj.isoformat()}

        return obj
    #_encode_datetime()

    def _decode_datetime(self, obj):
        """datetime decoder
        Check it out: https://pypi.python.org/pypi/msgpack-python/

        :param obj: arg description
        :type obj: type description
        :return:
        :rtype:
        """

        if b'__datetime__' in obj:
            obj = dateutil.parser.parse(obj[b"as_str"])

        logger.debug("obj: %s", obj)
        return obj
    #_decode_datetime()

#CodecSubBase


class CodecMsgpack(CodecSubBase):
    """Docstring for CodecMsgpack """

    def __init__(self):
        """todo: to be defined """
        super(CodecMsgpack, self).__init__('msgpack')
    #__init__()

    def decode(self, data):
        """todo: Docstring for decode

        :param data: arg description
        :type data: type description
        :return:
        :rtype:
        """
        logger.debug("data %s", data)
        return (not data) or \
            self._ser_cls.unpackb(data, object_hook=self._decode_datetime)
    #decode()

    def encode(self, data):
        """todo: Docstring for encode

        :param data: arg description
        :type data: type description
        :return:
        :rtype:
        """
        logger.debug("data %s", data)
        return self._ser_cls.packb(data, default=self._encode_datetime)
    #encode()
#CodecMsgpack


class CodecJSON(CodecSubBase):
    """Docstring for CodecJSON """

    def __init__(self):
        """todo: to be defined """
        super(CodecJSON, self).__init__('json')
    #__init__()

    def encode(self, data):
        """todo: Docstring for encode

        :param data: arg description
        :type data: type description
        :return:
        :rtype:
        """
        return self._ser_cls.dumps(data, default=self._encode_datetime)
    #encode()

    def decode(self, data):
        """todo: Docstring for decode

        :param data: arg description
        :type data: type description
        :return:
        :rtype:
        """
        return self._ser_cls.loads(data, object_hook=self._decode_datetime)
    #decode()
#CodecJSON


class CodecYaml(CodecSubBase):
    """Docstring for CodecYaml """

    def __init__(self):
        """todo: to be defined """
        super(CodecJSON, self).__init__('yaml')

        try:
            self._loader = self._ser_cls.CLoader
            self._dumper = self._ser_cls.CDumper
        except AttributeError:
            self._loader = self._ser_cls.Loader
            self._dumper = self._ser_cls.Dumper
    #__init__()

    def encode(self, data):
        """todo: Docstring for encode

        :param data: arg description
        :type data: type description
        :return:
        :rtype:
        """
        return self._ser_cls.dump(data, Dumper=self._dumper)
    #encode()

    def decode(self, data):
        """todo: Docstring for decode

        :param data: arg description
        :type data: type description
        :return:
        :rtype:
        """
        return self._ser_cls.load(data, Loader=self._loader)
    #decode()
#CodecYaml


class CodecPickle(CodecSubBase):
    """Docstring for CodecPickle """

    def __init__(self):
        """todo: to be defined """
        super(CodecJSON, self).__init__('pickle')
    #__init__()

    def encode(self, data):
        """todo: Docstring for encode

        :param data: arg description
        :type data: type description
        :return:
        :rtype:
        """
        return self._ser_cls.dumps(data)
    #encode()

    def decode(self, data):
        """todo: Docstring for decode

        :param data: arg description
        :type data: type description
        :return:
        :rtype:
        """
        return self._ser_cls.loads(data)
    #decode()
#CodecPickle

_CODEC_CLASSES = {
    'msgpack': CodecMsgpack,
    'json': CodecJSON,
    'yaml': CodecYaml,
    'pickle': CodecPickle,
}


class Codec(object):
    def __init__(self, fmt=None, sub_codec=None):
        """A simple, some what dynamic, wrapper
        around available codecs. This is our codec
        interface.
        :param fmt: name of codec to use
        :type fmt: String
        :param sub_codec: An existing sub codec instance
        :type fmt: SubCodecBase instance
        """

        logger.debug("fmt: %s, sub_codec: %s", fmt, sub_codec)

        self._fmt = fmt or 'msgpack'
        self._sub_codec = sub_codec

        if not self._sub_codec:
            self._sub_codec = _CODEC_CLASSES[self._fmt]()

        self._encode = self._sub_codec.encode
        self._decode = self._sub_codec.decode
    #__init__()

    def encode(self, data):
        return self._encode(data)
    #encode()

    def decode(self, data):
        return self._decode(data)
    #decode()
#Codec


def find_codec(fmt):
    try:
        return _CODEC_CACHE[fmt]
    except KeyError:
        _CODEC_CACHE[fmt] = Codec(fmt)

    return _CODEC_CACHE[fmt]
#find_codec()


class MsgBase(object):
    """Docstring for Msg """

    def __init__(self, payload=None, id=None, fmt=None, transport=None):
        """todo: to be defined

        :param ver: arg description
        :type ver: type description
        """
        logger.debug("payload: %s, id: %s, fmt: %s", payload, id, fmt)

        self._ver = self._ver or 0
        self._id = id or str(uuid4())
        self._fmt = fmt or 'msgpack'
        self._payload = payload or ''
        self._codec = find_codec(self._fmt)
        self._trans = transport or None
        self._msg = None
    #__init__()

    def __str__(self):
        return "\nVersion {}\nID      {}\nFormat  {}\nPayload {}".format(
            self._ver, self._id, self._fmt, self._payload)
    #__str__()

    def __repr__(self):
        return self.msg
    #__repr__()

    @property
    def id(self):
        return self._id
    #id()

    @id.setter
    def id(self, data=None, delay=False):
        self._id = data or str(uuid4())
        if not delay:
            self._msg = self.serialized
    #id()

    @property
    def ver(self):
        return self._ver
    #ver()

    @property
    def payload(self):
        return self._payload
    #payload()

    @payload.setter
    def payload(self, data, delay=False):
        self._payload = data
        if not delay:
            self._msg = self.serialized
    #payload()

    @property
    def fmt(self):
        return self._fmt
    #fmt()

    @fmt.setter
    def fmt(self, data, delay=False):
        self._fmt = data
        if not delay:
            self._msg = self.serialized
    #fmt()

    @property
    def msg(self):
        if not self._msg:
            self._msg = self.serialized

        return self._msg
    #msg()

    @property
    def transport(self):
        return self._trans
    #transport()

    @transport.setter
    def transport(self, data):
        self._trans = data
    #transport()

    @classmethod
    def decode(cls, msg, transport=None):
        logger.debug("msg: %s", msg)

        parts = msg.split(':', 3)
        fmt = parts[2]
        codec = find_codec(fmt)
        pl = parts[3]
        pl = pl and codec.decode(pl)
        return cls(pl, id=parts[1], fmt=fmt, transport=transport)
    #decode()

    @property
    def serialized(self):
        # The payload can be empty! A quick and cheesy way to
        # fire events.

        pl = self._payload and self._codec.encode(self._payload)
        return "{}:{}:{}:{}".format(self._ver, self._id, self._fmt, pl)
    #serialized()
#MsgBase
