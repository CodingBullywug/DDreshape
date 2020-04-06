from DD.utils import PoolByteArray2NumpyArray, NumpyArray2PoolByteArray
from DD.Entity import Entity
import numpy as np

class Terrain(Entity):
    def __init__(self, json, width, height, cell_res=[4, 4], terrain_types=4):
        super(Terrain, self).__init__(json)
        self.cell_res = cell_res
        self.terrain_types = terrain_types
        self.splat = PoolByteArray2NumpyArray(self._json['splat']).reshape(height*self.cell_res[1], width*self.cell_res[1], self.terrain_types, order='C')

    def get_json(self):
        json = self._json
        json['splat'] = NumpyArray2PoolByteArray(self.splat.reshape(np.prod(self.splat.shape), order='C'))
        return json

    def pad(self, top, bottom, left, right):
        self.splat = np.pad(self.splat, 
                            ((top*self.cell_res[0], bottom*self.cell_res[0]), (left*self.cell_res[1], right*self.cell_res[1]), (0,0)),
                            mode='edge')
    
    def fliplr(self, width):
        self.splat = np.fliplr(self.splat)
    
    def flipud(self, height):
        self.splat = np.flipud(self.splat)

    def rot90(self, width, height):
        self.splat = self._rot90_map(self.splat)
        # self.splat = np.rot90(self.splat, k=1)

    def rot180(self, width, height):
        self.splat = self._rot180_map(self.splat)
        # self.splat = np.rot90(self.splat, k=2)

    def rot270(self, width, height):
        self.splat = self._rot270_map(self.splat)
        # self.splat = np.rot90(self.splat, k=3)