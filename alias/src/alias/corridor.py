# Copyright (c) 2012, DangerOnTheRanger
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution. 


__author__ = "DangerOnTheRanger"
__date__ = "May 11, 2012 4:07:36 PM"


import os

import panda3d.core

import alias.utils


CORRIDOR_SIZE = 20.0
CORRIDOR_SCALE = 5.0


class Corridor(object):

    def __init__(self, corridor_type, position, rotation):

        self._type = corridor_type
        self._position = position
        self._rotation = rotation

    def load(self, window):

        self._model = window.loader.loadModel(os.path.join(alias.utils.get_data_directory(),
                                                           'models',
                                                           'corridors',
                                                           self._type))
        self._model.setScale(CORRIDOR_SCALE)

        self._model.setPos(self._position)
        self._model.setH(self._rotation)

        self._model.reparentTo(window.render)
        self._model.setTwoSided(True)
