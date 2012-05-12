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
__date__ = "May 11, 2012 3:43:12 PM"


import os

import panda3d.core


def get_data_directory():
    return os.path.normpath(os.path.join(
                                         os.path.dirname(os.path.abspath(__file__)),
                                         os.pardir,
                                         'data'))


def copy_vector(vector):
    return panda3d.core.Vec3(vector.getX(), vector.getY(), vector.getZ())
