from DD.utils import PoolByteArray2NumpyArray, NumpyArray2PoolByteArray
from DD.Entity import Entity
import numpy as np

class Terrain(Entity):
    def __init__(self, json, width, height, scale=4, terrain_types=4):
        super(Terrain, self).__init__(json)
        self._scale = scale
        self.terrain_types = terrain_types
        self.splat = PoolByteArray2NumpyArray(self._json['splat']).reshape(height*self._scale, width*self._scale, self.terrain_types, order='C')

    def get_json(self):
        json = self._json
        json['splat'] = NumpyArray2PoolByteArray(self.splat.reshape(np.prod(self.splat.shape), order='C'))
        return json

    def pad(self, top, bottom, left, right):
        self.splat = np.pad(self.splat, 
                            ((top*self._scale, bottom*self._scale), (left*self._scale, right*self._scale), (0,0)),
                            mode='edge')

    def crop(self, top, bottom, left, right):
        self.splat = self._crop_map_safe(self.splat, top, bottom, left, right, self._scale)
    
    def fliplr(self, width):
        self.splat = np.fliplr(self.splat)
    
    def flipud(self, height):
        self.splat = np.flipud(self.splat)

    def rot90(self, width, height):
        self.splat = self._rot90_map(self.splat)

    def rot180(self, width, height):
        self.splat = self._rot180_map(self.splat)

    def rot270(self, width, height):
        self.splat = self._rot270_map(self.splat)
