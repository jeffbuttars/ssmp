import pkgutil
import importlib

# Besure our toplevel dir is available for easy imports
# This is mostly for doing local development
import sys
import os

top_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../..'))
if top_path not in sys.path:
    sys.path.append(top_path)

# Import all sub transport packages.
for p in pkgutil.iter_modules(__path__, __name__ + "."):
    print("Adding local %s" % ([p[1].split('.')[-1]],))
    locals()[p[1].split('.')[-1]] = \
        importlib.import_module(p[1]).transport_class
