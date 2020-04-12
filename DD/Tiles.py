from DD.utils import PoolIntArray2NumpyArray, NumpyArray2PoolIntArray
from DD.Entity import Entity
import numpy as np

class Tiles(Entity):
    def __init__(self, json, width, height):
        super(Tiles, self).__init__(json)
        self.tiles = PoolIntArray2NumpyArray(self._json['cells']).reshape(height, width)
        self.colors = np.asarray(self._json['colors']).reshape(height, width)

    def get_json(self):
        json = self._json
        json['cells'] = NumpyArray2PoolIntArray(self.tiles.reshape(np.prod(self.tiles.shape)))
        json['colors'] = list(self.colors.reshape(np.prod(self.colors.shape)))
        return json

    def pad(self, top, bottom, left, right):
        self.tiles = np.pad(self.tiles, ((top, bottom), (left, right)), mode='constant', constant_values=-1)
        self.colors = np.pad(self.colors, ((top, bottom), (left, right)), mode='edge')

    def crop(self, top, bottom, left, right):
        self.tiles = self._crop_map_safe(self.tiles, top, bottom, left, right, 1)
        self.colors = self._crop_map_safe(self.colors, top, bottom, left, right, 1)
    
    def fliplr(self, width):
        self.tiles = np.fliplr(self.tiles)
        self.colors = np.fliplr(self.colors)
    
    def flipud(self, height):
        self.tiles = np.flipud(self.tiles)
        self.colors = np.flipud(self.colors)

    def rot90(self, width, height):
        self.tiles = self._rot90_map(self.tiles)
        self.colors = self._rot90_map(self.colors)

    def rot180(self, width, height):
        self.tiles = self._rot180_map(self.tiles)
        self.colors = self._rot180_map(self.colors)

    def rot270(self, width, height):
        self.tiles = self._rot270_map(self.tiles)
        self.colors = self._rot270_map(self.colors)
