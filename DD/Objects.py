from DD.utils import Vector22NumpyArray, NumpyArray2Vector2
from DD.Entity import Entity
import numpy as np

class Object(Entity):
    def __init__(self, json, width, height, scale=256):
        super(Object, self).__init__(json)
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

class Objects(Entity):
    def __init__(self, json, width, height, scale=256):
        super(Objects, self).__init__(json)
        self.scale = scale
        self.objects = [Object(object_json, width, height, scale=self.scale) for object_json in self._json]

    def get_json(self):
        json = self._json
        json = [obj.get_json() for obj in self.objects]
        return json

    def pad(self, top, bottom, left, right):
        for obj in self.objects:
            obj.pad(top, bottom, left, right)

    def crop(self, top, bottom, left, right):
        for obj in self.objects:
            obj.crop(top, bottom, left, right)

    def fliplr(self):
        for obj in self.objects:
            obj.fliplr()
    
    def flipud(self):
        for obj in self.objects:
            obj.flipud()

    def transpose(self):
        for obj in self.objects:
            obj.transpose()

    def rotate(self, angle):
        for obj in self.objects:
            obj.rotate(angle)
    