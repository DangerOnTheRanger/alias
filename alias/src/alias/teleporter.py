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
__date__ = "May 11, 2012 10:20:08 PM"


import os

import alias.utils
import alias.shadow


TELEPORTER_SCALE = 10.0
Z_OFFSET = 20.0


class StartTeleporter(object):

    def __init__(self, position):
        self._position = position

    def load(self, window):

        self._model = window.loader.loadModel(os.path.join(alias.utils.get_data_directory(),
                                                           'models',
                                                           'other',
                                                           'entry-teleport'))
        self._model.setPos(self._position)
        self._model.setZ(self._model.getZ() - Z_OFFSET)
        self._model.setScale(TELEPORTER_SCALE)
        self._model.reparentTo(window.render)

        self._shadow = alias.shadow.make_blob_shadow(2, window)
        self._shadow.reparentTo(self._model)
        self._shadow.setZ(0.01)

    @property
    def position(self):
        return self._position


class ExitTeleporter(object):

    def __init__(self, position):
        self._position = position

    def load(self, window, level):

        self._level = level

        self._model = window.loader.loadModel(os.path.join(alias.utils.get_data_directory(),
                                                           'models',
                                                           'other',
                                                           'exit-teleport'))
        self._model.setPos(self._position)
        self._model.setZ(self._model.getZ() - Z_OFFSET)
        self._model.setScale(TELEPORTER_SCALE)
        self._model.reparentTo(window.render)

        self._shadow = alias.shadow.make_blob_shadow(2, window)
        self._shadow.reparentTo(self._model)
        self._shadow.setZ(0.01)
