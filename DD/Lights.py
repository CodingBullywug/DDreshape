from DD.utils import Vector22NumpyArray, NumpyArray2Vector2
from DD.Entity import Entity
import numpy as np

class Light(Entity):
    def __init__(self, json, width, height, scale=256):
        super(Light, self).__init__(json)
        self.scale = scale
        self.position = Vector22NumpyArray(self._json['position'])

    def get_json(self):
        json = self._json
        json['position'] = NumpyArray2Vector2(self.position)
        return json

    def pad(self, top, bottom, left, right):
        self.position += np.asarray([left*self.scale, top*self.scale])

class Lights(Entity):
    def __init__(self, json, width, height, scale=256):
        super(Lights, self).__init__(json)
        self.scale = scale
        self.lights = [Light(light_json, width, height, scale=self.scale) for light_json in self._json]

    def get_json(self):
        json = self._json
        json = [light.get_json() for light in self.lights]
        return json

    def pad(self, top, bottom, left, right):
        for light in self.lights:
            light.pad(top, bottom, left, right)

    def crop(self, top, bottom, left, right):
        for light in self.lights:
            light.crop(top, bottom, left, right)

    def fliplr(self):
        for light in self.lights:
            light.fliplr()
    
    def flipud(self):
        for light in self.lights:
            light.flipud()

    def transpose(self):
        for light in self.lights:
            light.transpose()

    def rotate(self, angle):
        for light in self.lights:
            light.rotate(angle)
    