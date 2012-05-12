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


import os

import panda3d.core

import alias.utils


SPEED = 95
PLAYER_HEIGHT = 5
CAMERA_DISTANCE = 0
BULLET_DAMAGE = 25
BULLET_SPEED = 1000

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

        self._gun = self._window.loader.loadModel(os.path.join(alias.utils.get_data_directory(),
                                                  'models',
                                                  'weapons',
                                                  'pistol',
                                                  'pistol'))
        self._gun.reparentTo(self._node)
        self._gun.clearCompass()
        self._gun.setScale(0.5)
        self._gun.setX(2)
        self._gun.setY(6)
        self._gun.setZ(-1)
        self._gun.setCollideMask(panda3d.core.BitMask32(0x0))

        self._bullets = []
        self._window.taskMgr.add(self._bullet_movement_task, 'Bullet movement')

        self._collision_geometry = panda3d.core.CollisionSphere(0, 0, 0, PLAYER_HEIGHT / 2.0)
        self._collision_node = self._node.attachNewNode(panda3d.core.CollisionNode('player collision node'))
        self._collision_node.node().addSolid(self._collision_geometry)
        self._collision_node.node().setFromCollideMask(panda3d.core.GeomNode.getDefaultCollideMask())

        self._collision_handler = panda3d.core.CollisionHandlerPusher()
        self._window.cTrav.addCollider(self._collision_node, self._collision_handler)
        self._collision_handler.addCollider(self._collision_node, self._node)

        self._mouse_ray_node = self._window.camera.attachNewNode(panda3d.core.CollisionNode('mouse ray'))
        self._mouse_ray_node.node().setFromCollideMask(panda3d.core.GeomNode.getDefaultCollideMask())
        self._mouse_ray = panda3d.core.CollisionRay()
        self._mouse_ray_node.node().addSolid(self._mouse_ray)
        self._mouse_ray_handler = panda3d.core.CollisionHandlerQueue()
        self._window.cTrav.addCollider(self._mouse_ray_node, self._mouse_ray_handler)

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
        self._window.accept('mouse1', self._fire)

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
            self._node.setP(self._node.getP() - (mouse_y - self._window.win.getYSize() / 2) * 0.1)
            self._window.camera.setP(self._window.camera.getP() - (mouse_y - self._window.win.getYSize() / 2) * 0.1)

        return task.cont

    def _movement_task(self, task):

        time_since_last_frame = globalClock.getDt()
        self._node.setPos(self._node, panda3d.core.Vec3(self._movement_vector[0] * time_since_last_frame * SPEED,
                                                        self._movement_vector[1] * time_since_last_frame * SPEED,
                                                        0))
        self._node.setZ(PLAYER_HEIGHT)

        return task.cont

    def _fire(self):

        if self._window.mouseWatcherNode.hasMouse() is False:
            return

        mouse_position = self._window.mouseWatcherNode.getMouse()
        self._mouse_ray.setFromLens(self._window.camNode, mouse_position.getX(), mouse_position.getY())

        focus_point = None

        if self._mouse_ray_handler.getNumEntries() > 0:

            self._mouse_ray_handler.sortEntries()
            focus_point = self._mouse_ray_handler.getEntry(0).getSurfacePoint(self._window.render)

        bullet, bullet_collision_handler, bullet_collision_node = self._make_bullet()
        bullet.reparentTo(self._window.render)
        bullet.setPos(self._gun, 0, 5, 0)

        if focus_point is not None:
            bullet.lookAt(focus_point)

        self._bullets.append((bullet, bullet_collision_handler, bullet_collision_node))

    def _bullet_movement_task(self, task):

        for index, (bullet, bullet_collision_handler, bullet_collision_node) in list(enumerate(self._bullets)):

            if bullet_collision_handler.getNumEntries() > 0:

                bullet_collision_handler.sortEntries()
                colliding_object = bullet_collision_handler.getEntry(0).getIntoNodePath()
                colliding_object = colliding_object.findNetPythonTag('enemy')

                if colliding_object.isEmpty() is False:

                    enemy = colliding_object.getPythonTag()
                    enemy.take_damage(BULLET_DAMAGE)

                self._window.cTrav.removeCollider(bullet_collision_node)
                bullet.removeNode()
                del self._bullets[index]

            else:

                time_since_last_frame = globalClock.getDt()
                bullet.setY(bullet, BULLET_SPEED * time_since_last_frame)

        return task.cont

    def _make_bullet(self):

        card_maker = panda3d.core.CardMaker('bullet maker')
        BULLET_SIZE = 1.5
        card_maker.setFrame(-BULLET_SIZE / 2.0, BULLET_SIZE / 2.0, -BULLET_SIZE / 2.0, BULLET_SIZE / 2.0)
        card_maker.setHasUvs(True)

        bullet_geometry = card_maker.generate()
        bullet_texture = self._window.loader.loadTexture(os.path.join(alias.utils.get_data_directory(),
                                                                      'textures',
                                                                      'player-shot.png'))

        bullet_node = panda3d.core.NodePath(bullet_geometry)
        bullet_node.setTexture(bullet_texture)
        bullet_node.setTransparency(panda3d.core.TransparencyAttrib.MAlpha)
        bullet_node.setBillboardPointWorld()
        bullet_node.setCollideMask(panda3d.core.BitMask32(0x0))
        dummy_bullet_node = panda3d.core.NodePath('player_bullet')
        bullet_node.reparentTo(dummy_bullet_node)

        collision_geometry = panda3d.core.CollisionSphere(0, 0, 0, BULLET_SIZE / 2.0)
        collision_node = dummy_bullet_node.attachNewNode(panda3d.core.CollisionNode('bullet collision node'))
        collision_node.node().addSolid(collision_geometry)
        collision_node.node().setFromCollideMask(panda3d.core.GeomNode.getDefaultCollideMask())
        collision_handler = panda3d.core.CollisionHandlerQueue()

        self._window.cTrav.addCollider(collision_node, collision_handler)

        return dummy_bullet_node, collision_handler, collision_node
