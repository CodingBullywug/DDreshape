from DD.utils import Vector22NumpyArray, NumpyArray2Vector2, PoolVector2Array2NumpyArray, NumpyArray2PoolVector2Array
from DD.Entity import Entity
import numpy as np

class Path(Entity):
    def __init__(self, json, width, height, scale=256):
        super(Path, self).__init__(json)
        self._scale = scale
        self.rotation = self._json['rotation']
        self.position = Vector22NumpyArray(self._json['position'])
        self.edit_points = PoolVector2Array2NumpyArray(self._json['edit_points'])

    def get_json(self):
        json = self._json
        json['rotation'] = self.rotation
        json['position'] = NumpyArray2Vector2(self.position)
        json['edit_points'] = NumpyArray2PoolVector2Array(self.edit_points)
        return json

    def pad(self, top, bottom, left, right):
        self.position += np.asarray([left*self._scale, top*self._scale])

    def fliplr(self, width):
        self.position[0] = width*self._scale - self.position[0]
        v2 = self._rotate_vector(self.edit_points, self.rotation)
        v2[:,0] = -v2[:,0]
        self.edit_points = self._rotate_vector(v2, -self.rotation)
    
    def flipud(self, height):
        self.position[1] = height*self._scale - self.position[1]
        v2 = self._rotate_vector(self.edit_points, self.rotation)
        v2[:,1] = -v2[:,1]
        self.edit_points = self._rotate_vector(v2, -self.rotation)

    def rot90(self, width, height):
        self.position = self._rot90_point(self.position, self._scale, width, height)
        self.rotation = self.rotation - np.pi/2

class Paths(Entity):
    def __init__(self, json, width, height, scale=256):
        super(Paths, self).__init__(json)
        self._scale = scale
        self.paths = [Path(path_json, width, height, scale=self._scale) for path_json in self._json]

    def get_json(self):
        json = self._json
        json = [path.get_json() for path in self.paths]
        return json

    def pad(self, top, bottom, left, right):
        for path in self.paths:
            path.pad(top, bottom, left, right)

    def crop(self, top, bottom, left, right):
        for path in self.paths:
            path.crop(top, bottom, left, right)

    def fliplr(self, width):
        for path in self.paths:
            path.fliplr(width)
    
    def flipud(self, height):
        for path in self.paths:
            path.flipud(height)

    def transpose(self):
        for path in self.paths:
            path.transpose()

    def rotate(self, angle):
        for path in self.paths:
            path.rotate(angle)

    def rot90(self, width, height):
        for path in self.paths:
            path.rot90(width, height)
    