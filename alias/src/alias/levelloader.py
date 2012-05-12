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
__date__ = "May 11, 2012 3:22:17 PM"


import os

import panda3d.core
import Image

import alias.utils
import alias.corridor


BLACK = (0, 0, 0)
CORRIDOR = (146, 146, 146)
START_TELEPORTER = (0, 0, 255)
EXIT_TELEPORTER = (219, 146, 0)

X, Y = range(2)


def calculate_pixel_location(index, image_width, image_height):
    return (index % image_width, index / image_height)


def is_valid_coordinates(vector, image_width, image_height):

    if vector[X] < 0 or vector[X] > image_width - 1:
        return False

    if vector[Y] < 0 or vector[Y] > image_height - 1:
        return False

    return True


def place_corridor(level, corridor_type, rotation):
    pass


def determine_corridor_piece(image, pixel_location):

    top_neighbor = (pixel_location[X], pixel_location[Y] + 1)
    bottom_neighbor = (pixel_location[X], pixel_location[Y] - 1)
    left_neighbor = (pixel_location[X] - 1, pixel_location[Y])
    right_neighbor = (pixel_location[X] + 1, pixel_location[Y])

    neighbor_translation_string = ''

    for neighbor_coordinate in (top_neighbor, bottom_neighbor, left_neighbor, right_neighbor):

        if is_valid_coordinates(neighbor_coordinate) is False:

            neighbor_translation_string += '0'
            continue

        if image.getpixel(neighbor_coordinate[X], neighbor_coordinate[Y]) != BLACK:
            neighbor_translation_string += '1'

        else:
            neighbor_translation_string += '0'

    if neighbor_translation_string == '0000':
        raise RuntimeError, 'corridor with no neighbors'

    translation_table = {'1000' : (180, 'end'),
                         '0100' : (0, 'end'),
                         '0010' : (90, 'end'),
                         '0001' : (-90, 'end'),

                         '1100' : (0, 'straight'),
                         '0011' : (90, 'straight'),

                         '1001' : (-90, 'right-corner'),
                         '0101' : (0, 'right-corner'),

                         '1010' : (90, 'left-corner'),
                         '0110' : (0, 'left-corner'),

                         '1110' : (90, 'tee'),
                         '1101' : (-90, 'tee'),
                         '1011' : (180, 'tee'),
                         '0111' : (0, 'tee'),

                         '1111' : (0, 'four-way')
                         }

    return translation_table[neighbor_translation_string]


def load_level(level_name):

    corridor_map = Image.open(os.path.join(alias.utils.get_data_directory(),
                                            'levels',
                                            level_name,
                                            'corridor-map.png'))

    map_width, map_height = image.size
    corridor_position = panda3d.core.Vec3(-(map_width * alias.corridor.CORRIDOR_SIZE) / 2,
                                          - (map_height * alias.corridor.CORRIDOR_SIZE) / 2)

    pixels = list(corridor_map.getdata())

    for index, pixel in enumerate(pixels):

        if corridor_position.getX() >= (map_width * alias.corridor.CORRIDOR_SIZE) / 2:

            corridor_position.setX(-(map_width * alias.corridor.CORRIDOR_SIZE) / 2)
            corridor_position.setY(corridor_position.getY() + alias.corridor.CORRIDOR_SIZE)

        if pixel != BLACK:

            pixel_location = calculate_pixel_location(index, map_width, map_height)
            rotation, corridor_type = determine_corridor_piece(image, pixel_location)

            place_corridor(corridor_type, rotation)

        if pixel == START_TELEPORTER:



        corridor_position.setX(corridor_position.getX() + alias.corridor.CORRIDOR_SIZE)
