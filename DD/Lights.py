from DD.utils import Vector22NumpyArray, NumpyArray2Vector2
from DD.Entity import Entity
import numpy as np

class Light(Entity):
    def __init__(self, json, width, height, scale=256):
        super(Light, self).__init__(json)
        self._scale = scale
        self.position = Vector22NumpyArray(self._json['position'])

    def get_json(self):
        json = self._json
        json['position'] = NumpyArray2Vector2(self.position)
        return json

    def pad(self, top, bottom, left, right):
        self.position += np.asarray([left*self._scale, top*self._scale])

    def crop(self, top, bottom, left, right):
        self.position -= np.asarray([left*self._scale, top*self._scale])

    def fliplr(self, width):
        self.position[0] = width*self._scale - self.position[0]

    def flipud(self, height):
        self.position[1] = height*self._scale - self.position[1]

    def rot90(self, width, height):
        self.position = self._rot90_point(self.position, self._scale, width, height)

class Lights(Entity):
    def __init__(self, json, width, height, scale=256):
        super(Lights, self).__init__(json)
        self._scale = scale
        self.lights = [Light(light_json, width, height, scale=self._scale) for light_json in self._json]

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

    def fliplr(self, width):
        for light in self.lights:
            light.fliplr(width)
    
    def flipud(self, height):
        for light in self.lights:
            light.flipud(height)

    def transpose(self):
        for light in self.lights:
            light.transpose()

    def rotate(self, angle):
        for light in self.lights:
            light.rotate(angle)
    
    def rot90(self, width, height):
        for light in self.lights:
            light.rot90(width, height)

    # def rot180(self, width, height):
    #     for light in self.lights:
    #         light.rot180(width, height)
    
    # def rot270(self, width, height):
    #     for light in self.lights:
    #         light.rot270(width, height)