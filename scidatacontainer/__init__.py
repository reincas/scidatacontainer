##########################################################################
# Copyright (c) 2023 Reinhard Caspary                                    #
# <reinhard.caspary@phoenixd.uni-hannover.de>                            #
# This program is free software under the terms of the MIT license.      #
##########################################################################
#
# This package provides the Scientific Data Container as class Container
# which may be stored as a ZIP package containing items (files). Based
# on their file extension, the following item types are supported:
#
# .json: JSON file
# .txt:  Encoded text file (default encoding: UTF-8)
# .log:  Encoded text file (default encoding: UTF-8)
# .pgm:  Encoded text file (default encoding: UTF-8)
# .bin:  Raw binary data file
# .npy:  NumPy array (requires Python module numpy)
# .png:  PNG image (requires Python modules cv2 and numpy)
#
# Users may register other file extensions to file conversion classes
# using the function register(). See package fileimage as an example for
# such a conversion class.
#
##########################################################################

from importlib import import_module
from .filebase import FileBase
from .container import DataContainer, timestamp
from .container import MODELVERSION as version

suffixes = {}
classes = {}
formats = []


def register(suffix, fclass, pclass=None):

    """ Register a suffix to a conversion class. If the parameter class
    is a string, it is interpreted as known suffix and the conversion
    class of this suffix is registered also for the new one. """

    if isinstance(fclass, str):
        if not pclass is None:
            raise RuntimeError("Alias %s:%s with default class!" % (suffix, fclass))
        fclass = suffixes[fclass]

    # Simple sanity check for the class interface
    for method in ("encode", "decode", "hash"):
        if not hasattr(fclass, method) or not callable(getattr(fclass, method)):
            raise RuntimeError("No method %s() in class for suffix '%s'!" \
                               % (method, suffix))

    # Register suffix
    suffixes[suffix] = fclass

    # Register Python class. Last registration becomes default.
    # Overriding the mapping dict:JsonFile is not allowed.
    if pclass not in classes or not pclass is dict:
        classes[pclass] = fclass

    # Register unknown file format
    if fclass not in formats:
        formats.append(fclass)


# Initialize the conversion class database

for name in ("filebase", "fileimage", "filenumpy"):
    fullname = __name__ + "." + name
    try:
        module = import_module(fullname)
    except ModuleNotFoundError:
        #print("%s import failed" % fullname)
        continue
    #print("%s imported" % fullname)
    for suffix, fclass, pclass in module.register:
        register(suffix, fclass, pclass)

    
# Inject certain known file formats into the container class
class Container(DataContainer):

    """ Scientific data container. """

    _suffixes = suffixes
    _classes = classes
    _formats = formats
