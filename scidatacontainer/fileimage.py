##########################################################################
# Copyright (c) 2023 Reinhard Caspary                                    #
# <reinhard.caspary@phoenixd.uni-hannover.de>                            #
##########################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##########################################################################
#
# This module provides data conversion classes for image files. All
# data conversion classes should inherit from filebase.FileBase and must
# provide three methods:
#
# encode(): Return data encoded as bytes string.
# decode(data): Decode and store given bytes string data.
# hash(): Return SHA256 hash from data as hex string.
#
# The hash implementation shoud make sure that semantically equivalent
# data results in the same hash.
#
##########################################################################

import cv2 as cv
import numpy as np

from .filebase import FileBase


class PngFile(FileBase):

    """ Data conversion class for PNG image. """

    def encode(self):

        """ Convert image to bytes string. """

        return cv.imencode('.png', self.data)[1].tobytes()

    def decode(self, data):

        """ Decode image from bytes string. """

        flags = cv.IMREAD_ANYDEPTH | cv.IMREAD_ANYCOLOR
        self.data = np.frombuffer(data, dtype=np.uint8)
        self.data = cv.imdecode(self.data, flags=flags)
