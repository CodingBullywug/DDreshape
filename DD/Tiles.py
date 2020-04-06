from DD.utils import PoolIntArray2NumpyArray, NumpyArray2PoolIntArray
from DD.Entity import Entity
import numpy as np

class Tiles(Entity):
    def __init__(self, json, width, height):
        super(Tiles, self).__init__(json)
        self.tiles = PoolIntArray2NumpyArray(self._json).reshape(height, width)

    def get_json(self):
        return NumpyArray2PoolIntArray(self.tiles.reshape(np.prod(self.tiles.shape)))

    def pad(self, top, bottom, left, right):
        self.tiles = np.pad(self.tiles, ((top, bottom), (left, right)), mode='constant', constant_values=-1)

    def crop(self, top, bottom, left, right):
        self.tiles = self.tiles[top:-bottom,left:-right]
    
    def fliplr(self, width):
        self.tiles = np.fliplr(self.tiles)
    
    def flipud(self, height):
        self.tiles = np.flipud(self.tiles)

    def rot90(self, width, height):
        self.tiles = self._rot90_map(self.tiles)
        # self.tiles = np.rot90(self.tiles, k=1)

    def rot180(self, width, height):
        self.tiles = self._rot180_map(self.tiles)
        # self.tiles = np.rot90(self.tiles, k=2)

    def rot270(self, width, height):
        self.tiles = self._rot270_map(self.tiles)
        # self.tiles = np.rot90(self.tiles, k=3)
