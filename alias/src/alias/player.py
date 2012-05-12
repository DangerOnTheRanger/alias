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
__date__ = "May 12, 2012 12:26:03 AM"


import panda3d.core


SPEED = 95
PLAYER_HEIGHT = 5
CAMERA_DISTANCE = 0


class Player(object):

    def __init__(self, position):

        self._position = position
        self._movement_vector = [0, 0]

    def load(self, window, level):

        self._window = window

        self._node = panda3d.core.NodePath('Player node')
        self._node.reparentTo(self._window.render)
        self._node.setPos(self._position)
        self._node.setEffect(panda3d.core.CompassEffect.make(self._window.render))

        self._collision_geometry = panda3d.core.CollisionSphere(0, 0, 0, PLAYER_HEIGHT / 2.0)
        self._collision_node = self._node.attachNewNode(panda3d.core.CollisionNode('player collision node'))
        self._collision_node.node().addSolid(self._collision_geometry)
        self._collision_node.node().setFromCollideMask(panda3d.core.GeomNode.getDefaultCollideMask())

        self._collision_handler = panda3d.core.CollisionHandlerPusher()
        self._window.cTrav = panda3d.core.CollisionTraverser()
        self._window.cTrav.addCollider(self._collision_node, self._collision_handler)
        self._collision_handler.addCollider(self._collision_node, self._node)

        self._window.disableMouse()
        properties = panda3d.core.WindowProperties()
        properties.setCursorHidden(True)
        self._window.win.requestProperties(properties)
        self._window.camera.reparentTo(self._node)
        self._window.camera.lookAt(self._node)
        self._window.camera.setY(CAMERA_DISTANCE)
        self._window.taskMgr.add(self._mouselook_task, 'Mouselook')
        self._window.taskMgr.add(self._movement_task, 'Movement')

        self._window.accept('w', self._affect_movement_vector, [(0, 1)])
        self._window.accept('w-up', self._affect_movement_vector, [(0, -1)])
        self._window.accept('a', self._affect_movement_vector, [(-1, 0)])
        self._window.accept('a-up', self._affect_movement_vector, [(1, 0)])
        self._window.accept('s', self._affect_movement_vector, [(0, -1)])
        self._window.accept('s-up', self._affect_movement_vector, [(0, 1)])
        self._window.accept('d', self._affect_movement_vector, [(1, 0)])
        self._window.accept('d-up', self._affect_movement_vector, [(-1, 0)])

    def _affect_movement_vector(self, vector):

        self._movement_vector[0] += vector[0]
        if self._movement_vector[0] > 1:
            self._movement_vector[0] = 1
        elif self._movement_vector[0] < -1:
            self._movement_vector[0] = -1

        self._movement_vector[1] += vector[1]
        if self._movement_vector[1] > 1:
            self._movement_vector[1] = 1
        elif self._movement_vector[1] < -1:
            self._movement_vector[1] = -1

    def _mouselook_task(self, task):

        mouse = self._window.win.getPointer(0)
        mouse_x = mouse.getX()
        mouse_y = mouse.getY()

        if self._window.win.movePointer(0, self._window.win.getXSize() / 2, self._window.win.getYSize() / 2):

            self._node.setH(self._node.getH() - (mouse_x - self._window.win.getXSize() / 2) * 0.1)
            self._window.camera.setP(self._window.camera.getP() - (mouse_y - self._window.win.getYSize() / 2) * 0.1)

        return task.cont

    def _movement_task(self, task):

        time_since_last_frame = globalClock.getDt()
        self._node.setPos(self._node, panda3d.core.Vec3(self._movement_vector[0] * time_since_last_frame * SPEED,
                                                        self._movement_vector[1] * time_since_last_frame * SPEED,
                                                        0))
        self._node.setZ(PLAYER_HEIGHT)

        return task.cont
