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
__date__ = "May 12, 2012 2:41:56 AM"


import os

import panda3d.core

import alias.utils


def make_blob_shadow(diameter, window):

    card_maker = panda3d.core.CardMaker('blob shadow')
    card_maker.setFrame(-diameter / 2.0, diameter / 2.0, -diameter / 2.0, diameter / 2.0)
    card_maker.setColor(0, 0, 0, 1)
    card_maker.setHasUvs(True)

    shadow_geometry = card_maker.generate()
    shadow_texture = window.loader.loadTexture(os.path.join(alias.utils.get_data_directory(),
                                                            'textures',
                                                            'shadow.png'))

    shadow_node = panda3d.core.NodePath(shadow_geometry)
    shadow_node.setTexture(shadow_texture)
    shadow_node.setTransparency(panda3d.core.TransparencyAttrib.MAlpha)
    shadow_node.setP(90)
    shadow_node.setTwoSided(True)

    return shadow_node
