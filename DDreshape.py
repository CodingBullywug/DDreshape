#!/usr/bin/env python

import argparse
import json
import numpy as np
from DD import Map

import matplotlib.pyplot as plt

def reshape_dungeondraft_map(map_name, pad=[0, 0, 0, 0], fliplr=False, flipud=False, rot90=False, rot180=False, rot270=False, transpose=False):
    print('Input file: ', map_name)
    with open(map_name) as fob:
        map_json = json.load(fob)
    print('Map size (width * height): ',map_json['world']['width'], '*', map_json['world']['height'])

    map_name_out = ''.join(map_name.split('.')[0:-1])

    # Read map
    DDmap = Map.Map(map_json)

    # Apply transformations
    if (any(pad)):
        pad_top, pad_bottom, pad_left, pad_right = pad
        DDmap.pad(pad_top, pad_bottom, pad_left, pad_right)
        map_name_out += '__padded_' + str(pad_top) + '_' + str(pad_bottom) + '_' + str(pad_left) + '_' + str(pad_right)

    if (fliplr):
        DDmap.fliplr()
        map_name_out += '__flipped_lr'

    if (flipud):
        DDmap.flipud()
        map_name_out += '__flipped_ud'

    if (rot90):
        DDmap.rot90()
        map_name_out += '__rot90'

    if (rot180):
        DDmap.rot180()
        map_name_out += '__rot180'

    if (rot270):
        DDmap.rot270()
        map_name_out += '__rot270'

    if (transpose):
        DDmap.transpose()
        map_name_out += '__transposed'

    # Convert transformed map to json
    new_map_json = DDmap.get_json()

    map_name_out += '.' + map_name.split('.')[-1]
    print('Output file: ', map_name_out)
    print('Map size (width * height): ',new_map_json['world']['width'], '*', new_map_json['world']['height'])
    with open(map_name_out, 'w') as fob:
        json.dump(new_map_json, fob, indent='\t')

def pad_map(map_json, top=0, bottom=0, left=0, right=0):

    DDmap = Map.Map(map_json)
    DDmap.pad(top, bottom, left, right)
    new_map_json = DDmap.get_json()

    return new_map_json

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Reshape a DungeonDraft map.")
    parser.add_argument('map', help='Path to DungeonDraft map file.')
    parser.add_argument('--pad', nargs=4, type=int, default=[0, 0, 0, 0], help='Number of tiles to add as padding to the map. (Default: %(default) s, type: %(type)s).', metavar=('top','bottom','left','right'))
    parser.add_argument('--fliplr', action="store_true", help='Flip the left and right hand sides of the map. (Default: %(default) s)')
    parser.add_argument('--flipud', action="store_true", help='Flip the top and bottom of the map. (Default: %(default) s)')
    parser.add_argument('--rot90', action="store_true", help='Rotate map 90 degrees counter-clockwise. (Default: %(default) s)')
    parser.add_argument('--rot180', action="store_true", help='Rotate map 180 degrees counter-clockwise. (Default: %(default) s)')
    parser.add_argument('--rot270', action="store_true", help='Rotate map 270 degrees counter-clockwise. (Default: %(default) s)')
    parser.add_argument('--transpose', action="store_true", help='Flip map along diagonal (top-left to bottom right). (Default: %(default) s)')

    args = parser.parse_args()

    print('Parsed arguments:')
    print(args)

    reshape_dungeondraft_map(map_name=args.map, pad=args.pad, fliplr=args.fliplr, flipud=args.flipud, rot90=args.rot90, rot180=args.rot180, rot270=args.rot270, transpose=args.transpose)
