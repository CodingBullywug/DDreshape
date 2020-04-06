from DD.utils import Vector22NumpyArray, NumpyArray2Vector2, PoolVector2Array2NumpyArray, NumpyArray2PoolVector2Array
from DD.Entity import Entity
import numpy as np

class Portal(Entity):
    def __init__(self, json, width, height, scale=256):
        super(Portal, self).__init__(json)
        self.scale = scale
        self.rotation = self._json['rotation']
        self.position = Vector22NumpyArray(self._json['position'])

    def get_json(self):
        json = self._json
        json['rotation'] = self.rotation
        json['position'] = NumpyArray2Vector2(self.position)
        return json

    def pad(self, top, bottom, left, right):
        self.position += np.asarray([left*self.scale, top*self.scale])

class Portals(Entity):
    def __init__(self, json, width, height, scale=256):
        super(Portals, self).__init__(json)
        self.scale = scale
        self.portals = [Portal(portal_json, width, height, scale=self.scale) for portal_json in self._json]

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

    def fliplr(self):
        for portal in self.portals:
            portal.fliplr()
    
    def flipud(self):
        for portal in self.portals:
            portal.flipud()

    def transpose(self):
        for portal in self.portals:
            portal.transpose()

    def rotate(self, angle):
        for portal in self.portals:
            portal.rotate(angle)
    