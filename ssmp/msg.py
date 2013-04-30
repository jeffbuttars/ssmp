import os
import re
import imp

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

_latest_version = None
version_objs = None


def versions():
    """todo: Docstring for versions
    :return:
    :rtype:
    """

    vers = []
    directory = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'msgs')
    # logger.debug(directory)

    for fname in os.listdir(directory):
        f = os.path.join(directory, fname)
        # logger.debug("checking %s", f)
        if os.path.isfile(f) and not os.path.islink(f):
            # logger.debug(f)
            m = re.match('^msg_v(\d+)\.(py|pyc|pyo)$', fname)
            if m:
                vers.append(int(m.groups()[0]))

    assert vers, "Unable to find any msg versions."
    vers.sort()
    return vers
#versions()


def latest_version():
    """Get the latest protocol version available
    :return: Most recent version
    :rtype: int
    """

    global _latest_version
    if not _latest_version:
        _latest_version = versions()[-1]

    return _latest_version
#latest_version()


class VersionObjects(object):

    def __init__(self):
        """todo: to be defined """
        self._versions = {}
    #__init__()

    def get(self, ver=None):
        """todo: Docstring for get

        :param ver: arg description
        :type ver: type description
        :return:
        :rtype:
        """

        # logger.debug("ver: %s", ver)
        v = ver or latest_version()
        # logger.debug("v: %s", v)

        try:
            return self._versions[v]
        except KeyError:

            directory = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'msgs')

            mod = 'msg_v{}'.format(v)
            # mod_path = os.path.join(directory, mod)
            mod_path = directory

            # We expect the mod to exist because latest_version()
            # does for us.
            # logger.debug("mod: %s, mod_path: %s", mod, mod_path)
            # logger.debug("find_module: %s", imp.find_module(mod, [mod_path]))
            vm = imp.load_module(mod, *imp.find_module(mod, [mod_path]))

            self._versions[v] = vm.Msg
            return vm.Msg
    #get()
#VersionObjects
version_objs = VersionObjects()


# Add our msgs dir to the sys.path
import sys
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'msgs'))


def Msg(*args, **kwargs):

    logger.debug("args: %s, kwargs: %s", args, kwargs)

    if 'ver' in kwargs:
        return version_objs.get(kwargs['ver']).Msg(*args, **kwargs)

    return version_objs.get().Msg(*args, **kwargs)
#Msg


def main():
    print("Latest Version : {}".format(version_objs.get()()))

    print("Available Versions :")
    for v in versions():
        m = version_objs.get(v)
        print("\t{}".format(m()))
    # end for v in  versions()
# main()

if __name__ == '__main__':
    main()
