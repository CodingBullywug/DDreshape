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
    