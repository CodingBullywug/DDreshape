import copy

from DD.utils import Vector22NumpyArray, NumpyArray2Vector2, PoolVector2Array2NumpyArray, NumpyArray2PoolVector2Array
from DD.Entity import Entity
import numpy as np

class Portal(Entity):
    def __init__(self, json, width, height, scale=256):
        super(Portal, self).__init__(json)
        self._scale = scale
        self.scale = Vector22NumpyArray(self._json['scale'])
        self.direction = Vector22NumpyArray(self._json['direction'])
        self.rotation = self._json['rotation']
        self.position = Vector22NumpyArray(self._json['position'])

    def get_json(self):
        json = self._json
        json['rotation'] = self.rotation
        json['position'] = NumpyArray2Vector2(self.position)
        json['direction'] = NumpyArray2Vector2(self.direction)
        # json['direction'] = NumpyArray2Vector2(np.asarray([np.cos(self.rotation), np.sin(self.rotation)]))
        json['scale'] = NumpyArray2Vector2(self.scale)

        return json

    def pad(self, top, bottom, left, right):
        self.position += np.asarray([left*self._scale, top*self._scale])

    def crop(self, top, bottom, left, right):
        self.position -= np.asarray([left*self._scale, top*self._scale])

    def fliplr(self, width):
        self.position[0] = width*self._scale - self.position[0]
        self.rotation = np.pi - self.rotation
        self.scale[1] = -1*self.scale[1]
        self.direction = np.asarray([np.cos(self.rotation), np.sin(self.rotation)])
    
    def flipud(self, height):
        # self.direction = -1*self.direction
        self.position[1] = height*self._scale - self.position[1]
        self.rotation = -1*self.rotation
        self.scale[1] = -1*self.scale[1]
        self.direction = np.asarray([np.cos(self.rotation), np.sin(self.rotation)])

    def rot90(self, width, height):
        self.position = self._rot90_point(self.position, self._scale, width, height)
        self.rotation = self.rotation - np.pi/2
        self.direction = np.asarray([np.cos(self.rotation), np.sin(self.rotation)])

class Portals(Entity):
    def __init__(self, json, width, height, scale=256):
        super(Portals, self).__init__(json)
        self._scale = scale
        self.portals = [Portal(portal_json, width, height, scale=self._scale) for portal_json in self._json]

    def get_json(self):
        json = self._json
        json = [portal.get_json() for portal in self.portals]
        return json

    def pad(self, top, bottom, left, right):
        for portal in self.portals:
            portal.pad(top, bottom, left, right)
    
    def crop(self, top, bottom, left, right):
        for portal in self.portals:
            portal.crop(top, bottom, left, right)

    def fliplr(self, width):
        for portal in self.portals:
            portal.fliplr(width)
    
    def flipud(self, height):
        for portal in self.portals:
            portal.flipud(height)

    def transpose(self):
        for portal in self.portals:
            portal.transpose()

    def rotate(self, angle):
        for portal in self.portals:
            portal.rotate(angle)

    def rot90(self, width, height):
        for portal in self.portals:
            portal.rot90(width, height)
    