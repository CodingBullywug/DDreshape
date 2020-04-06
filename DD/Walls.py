import copy

from DD.utils import PoolVector2Array2NumpyArray, NumpyArray2PoolVector2Array
from DD.Entity import Entity
from DD.Portals import Portals
import numpy as np

class Wall(Entity):
    def __init__(self, json, width, height, scale=256):
        super(Wall, self).__init__(json)
        self._scale = scale
        self.points = PoolVector2Array2NumpyArray(self._json['points'])
        self.portals = Portals(self._json['portals'], width, height, scale)

    def get_json(self):
        json = self._json
        json['points'] = NumpyArray2PoolVector2Array(self.points)
        json['portals'] = self.portals.get_json()
        return json

    def pad(self, top, bottom, left, right):
        self.points += np.asarray([left*self._scale, top*self._scale])
        self.portals.pad(top, bottom, left, right)

    def fliplr(self, width):
        self.points[:,0] = width*self._scale - self.points[:,0]
        self.portals.fliplr(width)
    
    def flipud(self, height):
        self.points[:,1] = height*self._scale - self.points[:,1]
        self.portals.flipud(height)

    def rot90(self, width, height):
        # _points = copy.deepcopy(self.points)
        # self.points[:,1] = width*self._scale - _points[:,0]
        # self.points[:,0] = _points[:,1]

        self.points = self._rot90_vector(self.points, self._scale, width, height)

        self.portals.rot90(width, height)

class Walls(Entity):
    def __init__(self, json, width, height, scale=256):
        super(Walls, self).__init__(json)
        self._scale = scale
        self.walls = [Wall(wall_json, width, height, scale=self._scale) for wall_json in self._json]

    def get_json(self):
        json = self._json
        json = [wall.get_json() for wall in self.walls]
        return json

    def pad(self, top, bottom, left, right):
        for wall in self.walls:
            wall.pad(top, bottom, left, right)

    def crop(self, top, bottom, left, right):
        for wall in self.walls:
            wall.crop(top, bottom, left, right)

    def fliplr(self, width):
        for wall in self.walls:
            wall.fliplr(width)
    
    def flipud(self, height):
        for wall in self.walls:
            wall.flipud(height)

    def transpose(self):
        for wall in self.walls:
            wall.transpose()

    def rotate(self, angle):
        for wall in self.walls:
            wall.rotate(angle)

    def rot90(self, width, height):
        for wall in self.walls:
            wall.rot90(width, height)
    