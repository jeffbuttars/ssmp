import pkgutil
import importlib


# Import all sub transport packages.
for p in pkgutil.iter_modules(__path__, __name__ + "."):
    locals()[p[1].split('.')[-1]] = \
        importlib.import_module(p[1]).transport_class
