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
__date__ = "May 11, 2012 8:27:57 PM"


import panda3d.core
import panda3d.ai

import alias.utils
import alias.player


class Level(object):

    def __init__(self, window):

        self._window = window
        self._ai_world = panda3d.ai.AIWorld(self._window.render)
        self._corridors = []
        self._enemies = []

    def add_corridor(self, corridor):
        self._corridors.append(corridor)

    def add_enemy(self, enemy):
        self._enemies.append(enemy)

    def set_start_teleporter(self, teleporter):
        self._start_teleporter = teleporter

    def set_exit_teleporter(self, teleporter):
        self._exit_teleporter = teleporter

    def load(self):

        for corridor in self._corridors:
            corridor.load(self._window)

        self._window.cTrav = panda3d.core.CollisionTraverser()

        for enemy in self._enemies:
            enemy.load(self._window, self._ai_world)

        self._start_teleporter.load(self._window)
        self._exit_teleporter.load(self._window, self)

        self._load_player()

        self._window.taskMgr.add(self._update_ai, 'AI update loop')

    def teardown(self):

        self._teardown_player()

        for enemy in self._enemies:
            enemy.teardown()

        for corridor in self._corridors:
            corridor.teardown()

        self._start_teleporter.teardown()
        self._exit_teleporter.teardown()

    def _update_ai(self, task):

        self._ai_world.update()
        return task.cont

    def _load_player(self):

        self._player = alias.player.Player(alias.utils.copy_vector(self._start_teleporter.position))
        self._player.load(self._window, self)

    def _teardown_player(self):
        pass
