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
__date__ = "May 11, 2012 8:55:39 PM"


import sys

import panda3d.core
from direct.showbase.ShowBase import ShowBase

import alias.levelloader


def main():

    panda3d.core.loadPrcFileData('', 'show-frame-rate-meter #t')
    panda3d.core.loadPrcFileData('', 'want-pstats #t')

    window = ShowBase()
    level = alias.levelloader.load_level(sys.argv[1], window)
    level.load()

    window.run()

if __name__ == '__main__':
    main()
