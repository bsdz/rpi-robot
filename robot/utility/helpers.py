'''
rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''

def range_bound(value, minimum, maximum):
    """bound value between minimum and maximum"""
    return min(max(value, minimum), maximum)