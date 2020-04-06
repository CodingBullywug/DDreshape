from DD.utils import PoolVector2Array2NumpyArray, NumpyArray2PoolVector2Array
from DD.Entity import Entity
import numpy as np

class Puddle(Entity):
    def __init__(self, json, width, height, scale):
        super(Puddle, self).__init__(json)
        self._scale = scale
        self.polygon = PoolVector2Array2NumpyArray(self._json['polygon'])
        self.puddles = [Puddle(puddle, width, height, scale) for puddle in self._json['children']]

    def get_json(self):
        json = self._json
        json['polygon'] = NumpyArray2PoolVector2Array(self.polygon)
        json['children'] = [puddle.get_json() for puddle in self.puddles]
        return json

    def pad(self, top, bottom, left, right):
        self.polygon += [left*self._scale, top*self._scale]
        for puddle in self.puddles:
            puddle.pad(top, bottom, left, right)

    def crop(self, top, bottom, left, right):
        self.polygon -= [left*self._scale, top*self._scale]
        for puddle in self.puddles:
            puddle.crop(top, bottom, left, right)
    
    def fliplr(self, width):
        self.polygon[:,0] = width*self._scale - self.polygon[:,0]
        for puddle in self.puddles:
            puddle.fliplr(width)
    
    def flipud(self, height):
        self.polygon[:,1] = height*self._scale - self.polygon[:,1]
        for puddle in self.puddles:
            puddle.flipud(height)

    def rot90(self, width, height):
        self.polygon = self._rot90_vector(self.polygon, self._scale, width, height)
        for puddle in self.puddles:
            puddle.rot90(width, height)

class Water(Entity):
    def __init__(self, json, width, height, scale=256):
        super(Water, self).__init__(json)
        self.has_tree = False
        if ('tree' in self._json):
            self.puddles = Puddle(self._json['tree'], width, height, scale)
        else:
            self.puddles = None

    def get_json(self):
        json = self._json
        if (self.puddles is not None):
            json['tree'] = self.puddles.get_json()
        return json

    def pad(self, top, bottom, left, right):
        if (self.puddles is not None):
            self.puddles.pad(top, bottom, left, right)

    def crop(self, top, bottom, left, right):
        if (self.puddles is not None):
            self.puddles.crop(top, bottom, left, right)

    def fliplr(self, width):
        if (self.puddles is not None):
            self.puddles.fliplr(width)
    
    def flipud(self, height):
        if (self.puddles is not None):
            self.puddles.flipud(height)

    def rot90(self, width, height):
        if (self.puddles is not None):
            self.puddles.rot90(width, height)
            