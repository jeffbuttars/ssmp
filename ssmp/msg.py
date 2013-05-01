import os
import re
import imp

import logging

# Set up the logger
logger = logging.getLogger('ssmp')
# Use a console handler, set it to debug by default
logger_ch = logging.StreamHandler()
logger.setLevel(logging.INFO)
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

    vers = {}
    directory = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'msgs')
    # logger.debug(directory)

    for fname in os.listdir(directory):
        f = os.path.join(directory, fname)
        # logger.debug("checking %s", f)
        if os.path.isfile(f) and not os.path.islink(f):
            # logger.debug(f)
            m = re.match('^msg_([\w_]+)\.(py|pyc|pyo)$', fname)
            if m:
                vers[m.groups()[0]] = None

    assert vers, "Unable to find any msg versions."

    return vers
#versions()


class VersionObjects(object):

    def __init__(self):
        """todo: to be defined """
        self._versions = {}
    #__init__()

    def get(self, ver='basic'):
        """todo: Docstring for get

        :param ver: arg description
        :type ver: type description
        :return:
        :rtype:
        """

        logger.debug("ver :%s", ver)

        try:
            return self._versions[ver]
        except KeyError:

            directory = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'msgs')

            mod = 'msg_{}'.format(ver)
            mod_path = directory

            vm = imp.load_module(mod, *imp.find_module(mod, [mod_path]))

            self._versions[ver] = vm.Msg
            return vm.Msg
    #get()
#VersionObjects
version_objs = VersionObjects()


# Add our msgs dir to the sys.path
import sys
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'msgs'))


# def main():
#     print("Latest Version : {}".format(version_objs.get()()))

#     print("Available Versions :")
#     for v in versions():
#         m = version_objs.get(v)
#         print("\t{}".format(m()))
#     # end for v in  versions()
# # main()

# if __name__ == '__main__':
#     main()
