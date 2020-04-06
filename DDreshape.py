#!/usr/bin/env python

import argparse
import json
import numpy as np

import matplotlib.pyplot as plt

# Helper functions for converting between data types
def PoolByteArray2NumpyArray(pool_byte_array_string):
    return np.array(pool_byte_array_string[14:-1].split(',')).astype(np.uint8)

def PoolIntArray2NumpyArray(pool_int_array_string):
    return np.array(pool_int_array_string[13:-1].split(',')).astype(np.int64)

def PoolVector2Array2NumpyArray(pool_vector2_array_string, dtype=np.float):
    np_array = np.array(pool_vector2_array_string[17:-1].split(',')).astype(dtype)
    return np_array.reshape(int(np_array.shape[0]/2),2)

def Vector22NumpyArray(vector2_string, dtype=np.float):
    return np.array(vector2_string[8:-1].split(',')).astype(dtype)

def NumpyArray2PoolByteArray(numpy_array):
    return 'PoolByteArray(' + ', '.join(list(numpy_array.astype(np.str))) + ')'

def NumpyArray2PoolIntArray(numpy_array):
    return 'PoolIntArray(' + ', '.join(list(numpy_array.astype(np.str))) + ')'

def NumpyArray2PoolVector2Array(numpy_array):
    return 'PoolVector2Array(' + ', '.join(list(numpy_array.flatten().astype(np.str))) + ')'

def NumpyArray2Vector2(numpy_array):
    return 'Vector2(' + ', '.join(list(numpy_array.astype(np.str))) + ')'

def NumpyByteArray2NumpyBitArray(np_byte_array, width, height):
    np_bit_str = ''.join(["{0:08b}".format(b) for b in np_byte_array])
    np_bit_flat = np.asarray(list(np_bit_str)).astype(np.uint8)
    np_bit_array = np.fliplr(np_bit_flat.reshape(len(np_byte_array),8)).reshape(len(np_bit_flat))[0:(width*height)].reshape(height, width)
    return np_bit_array

def NumpyBitArray2NumpyByteArray(np_bit_array):
    np_bit_array_flat = np_bit_array.flatten()
    np_bit_array_flat_padded = np.pad(np_bit_array_flat, (0,int(np.ceil(len(np_bit_array_flat)/8)*8-len(np_bit_array_flat))), mode='constant', constant_values=0) # Pad with zeros in the end to match byte size. Must be divisible by 8.
    np_bit_array_flat_padded_flipped = np.fliplr(np_bit_array_flat_padded.reshape(int(len(np_bit_array_flat_padded)/8),8))
    np_byte_array = np.asarray([int(''.join(list(row)),2) for row in np_bit_array_flat_padded_flipped.astype(str)])
    return np_byte_array

def reshape_dungeondraft_map(map_name, top=0, bottom=0, left=0, right=0):
    print('Input file: ', map_name)
    with open(map_name) as fob:
        map_json = json.load(fob)
    print('Map size (width * height): ',map_json['world']['width'], '*', map_json['world']['height'])
    
    map_padded_json = pad_map(map_json, top=top, bottom=bottom, left=left, right=right)

    map_name_out = ''.join(map_name.split('.')[0:-1]) + '__padded_' + str(top) + '_' + str(bottom) + '_' + str(left) + '_' + str(right) + '.' + map_name.split('.')[-1]
    print('Output file: ', map_name_out)
    with open(map_name_out, 'w') as fob:
        json.dump(map_padded_json, fob, indent='\t')

def pad_map(map_json, top=0, bottom=0, left=0, right=0):

    def pad_cave(cave_json, width, height, top=0, bottom=0, left=0, right=0):
    
        bitmap_width = width*4+3
        bitmap_height = height*4+3

        bytemap = PoolByteArray2NumpyArray(cave_json['bitmap'])
        bitmap = NumpyByteArray2NumpyBitArray(bytemap, bitmap_width, bitmap_height)
        bitmap_padded = np.pad(bitmap, ((4*top, 4*bottom), (4*left, 4*right)), mode='constant', constant_values=0)
        bytemap_padded = NumpyBitArray2NumpyByteArray(bitmap_padded)
        cave_json['bitmap'] = NumpyArray2PoolByteArray(bytemap_padded)
        return cave_json

    def pad_lights(lights_json, width, height, top=0, bottom=0, left=0, right=0):

        for light_json in lights_json:
            position = Vector22NumpyArray(light_json['position'])
            light_json['position'] = NumpyArray2Vector2(pad_vector(position, 256*top, 256*left))

        return lights_json

    def pad_materials(materials_json, width, height, top=0, bottom=0, left=0, right=0):

        bitmap_width = width*2+3
        bitmap_height = height*2+3

        for layer in materials_json:
            layer_json = materials_json[layer]
            for material in layer_json:
                bytemap = PoolByteArray2NumpyArray(material['bitmap'])
                bitmap = NumpyByteArray2NumpyBitArray(bytemap, bitmap_width, bitmap_height)
                bitmap_padded = np.pad(bitmap, ((2*top, 2*bottom), (2*left, 2*right)), mode='constant', constant_values=0)
                bytemap_padded = NumpyBitArray2NumpyByteArray(bitmap_padded)
                material['bitmap'] = NumpyArray2PoolByteArray(bytemap_padded)

        return materials_json

    def pad_objects(objects_json, width, height, top=0, bottom=0, left=0, right=0):

        for object_json in objects_json:
            position = Vector22NumpyArray(object_json['position'])
            object_json['position'] = NumpyArray2Vector2(pad_vector(position, 256*top, 256*left))

        return objects_json

    def pad_paths(paths_json, width, height, top=0, bottom=0, left=0, right=0):


        for path_json in paths_json:
            position = Vector22NumpyArray(path_json['position'])
            path_json['position'] = NumpyArray2Vector2(pad_vector(position, 256*top, 256*left))

        return paths_json

    def pad_portals(portals_json, width, height, top=0, bottom=0, left=0, right=0):

        for portal_json in portals_json:
            position = Vector22NumpyArray(portal_json['position'])
            portal_json['position'] = NumpyArray2Vector2(pad_vector(position, 256*top, 256*left))

        return portals_json

    def pad_shapes(shapes_json, width, height, top=0, bottom=0, left=0, right=0):
        #NOTE: Must be done as one-liner
        shapes_json['polygons'] = [NumpyArray2PoolVector2Array(PoolVector2Array2NumpyArray(polygon)+[256*left, 256*top]) for polygon in shapes_json['polygons']]
        return shapes_json

    def pad_terrain(terrain_json, width, height, top=0, bottom=0, left=0, right=0):

        terrain = PoolByteArray2NumpyArray(terrain_json['splat']).reshape(height*4, width*4, 4, order='C')
        terrain_padded = np.pad(terrain, ((top*4, bottom*4), (left*4, right*4), (0,0)), mode='edge')
        terrain_json['splat'] = NumpyArray2PoolByteArray(terrain_padded.reshape(np.prod(terrain_padded.shape), order='C'))

        return terrain_json

    def pad_tiles(tiles_json, width, height, top=0, bottom=0, left=0, right=0):
        tiles = PoolIntArray2NumpyArray(tiles_json).reshape(height, width)
        tiles_padded = np.pad(tiles, ((top, bottom), (left, right)), mode='constant', constant_values=-1)
        tiles_json = NumpyArray2PoolIntArray(tiles_padded.reshape(np.prod(tiles_padded.shape)))

        return tiles_json

    def pad_walls(walls_json, width, height, top=0, bottom=0, left=0, right=0):

        return [pad_wall(wall_json, width=width, height=height, top=top, bottom=bottom, left=left, right=right) for wall_json in walls_json]

    def pad_wall(wall_json, width, height, top=0, bottom=0, left=0, right=0):

        wall_json['points'] = NumpyArray2PoolVector2Array(PoolVector2Array2NumpyArray(wall_json['points'])+[256*left, 256*top])
        wall_json['portals'] = pad_portals(wall_json['portals'], width=width, height=height, top=top, bottom=bottom, left=left, right=right)

        return wall_json

    def pad_water(water_json, width, height, top=0, bottom=0, left=0, right=0):

        # NOTE: Not handling children of children, as they appear empty.
        if ('tree' in water_json):
            for child_json in water_json['tree']['children']:
                child_json['polygon'] = NumpyArray2PoolVector2Array(PoolVector2Array2NumpyArray(child_json['polygon'])+[256*left, 256*top])

        return water_json

    def pad_vector(vector, top=0, left=0):
        return vector + np.asarray([left, top])
    
    # Store old world size
    map_width = map_json['world']['width']
    map_height = map_json['world']['height']
    
    # Loop through each level and pad each element type
    for level in map_json['world']['levels']:
        level_json = map_json['world']['levels'][level]

        # Update each element
        level_json['cave'] = pad_cave(level_json['cave'], width=map_width, height=map_height, top=top, bottom=bottom, left=left, right=right)
        level_json['lights'] = pad_lights(level_json['lights'], width=map_width, height=map_height, top=top, bottom=bottom, left=left, right=right)
        level_json['materials'] = pad_materials(level_json['materials'], width=map_width, height=map_height, top=top, bottom=bottom, left=left, right=right)
        level_json['objects'] = pad_objects(level_json['objects'], width=map_width, height=map_height, top=top, bottom=bottom, left=left, right=right)
        level_json['paths'] = pad_paths(level_json['paths'], width=map_width, height=map_height, top=top, bottom=bottom, left=left, right=right)
        level_json['portals'] = pad_portals(level_json['portals'], width=map_width, height=map_height, top=top, bottom=bottom, left=left, right=right)
        level_json['shapes'] = pad_shapes(level_json['shapes'], width=map_width, height=map_height, top=top, bottom=bottom, left=left, right=right)
        level_json['terrain'] = pad_terrain(level_json['terrain'], width=map_width, height=map_height, top=top, bottom=bottom, left=left, right=right)
        level_json['tiles'] = pad_tiles(level_json['tiles'], width=map_width, height=map_height, top=top, bottom=bottom, left=left, right=right)
        level_json['walls'] = pad_walls(level_json['walls'], width=map_width, height=map_height, top=top, bottom=bottom, left=left, right=right)
        level_json['water'] = pad_water(level_json['water'], width=map_width, height=map_height, top=top, bottom=bottom, left=left, right=right)
        
        map_json['world']['levels'][level] = level_json

    # Update world to new size
    map_json['world']['width'] = map_width + left + right
    map_json['world']['height'] = map_height + top + bottom

    # Move camera position to center on same point
    camera_position = Vector22NumpyArray(map_json['header']['editor_state']['camera_position'])
    map_json['header']['editor_state']['camera_position'] = NumpyArray2Vector2(pad_vector(camera_position, 256*top, 256*left))

    return map_json

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Reshape a DungeonDraft map.")
    parser.add_argument('map', help='Path to DungeonDraft map file.')
    parser.add_argument('top', nargs='?', type=int, default=0, help='Number of tiles to add to the top of the map (Default: %(default) s, type: %(type)s).')
    parser.add_argument('bottom', nargs='?', type=int, default=0, help='Number of tiles to add to the bottom of the map (Default: %(default) s, type: %(type)s).')
    parser.add_argument('left', nargs='?', type=int, default=0, help='Number of tiles to add to the left of the map (Default: %(default) s, type: %(type)s).')
    parser.add_argument('right', nargs='?', type=int, default=0, help='Number of tiles to add to the right of the map (Default: %(default) s, type: %(type)s).')

    args = parser.parse_args()

    print('Parsed arguments:')
    print(args)

    reshape_dungeondraft_map(map_name=args.map, top=args.top, bottom=args.bottom, left=args.left, right=args.right)

    pass