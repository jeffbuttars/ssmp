import uuid4


class MsgBase(object):
    """Docstring for Msg """

    def __init__(self, msg=None, id=None):
        """todo: to be defined

        :param ver: arg description
        :type ver: type description
        """

        self._ver = 0
        self._msg = msg
        self._id = id and uuid4()
    #__init__()

    def __str__(self):
        """todo: Docstring for __repr__
        :return:
        :rtype:
        """
        return "SSMP Msg version {}".format(self._ver)
    #__str__()

    def __repr__(self):
        return self._msg
    #__repr__()

    @property
    def id(self):
        return str(self._id)
    #id()

    @property
    def msg(self):
        return self._msg
    #msg()

    @property
    def ver(self):
        return self._ver
    #ver()

    def send(self, msg=None, id=None):
        """todo: Docstring for send

        :param msg: arg description
        :type msg: type description
        :return:
        :rtype:
        """

        pass
    #send()
#MsgBase
