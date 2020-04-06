from DD.utils import PoolByteArray2NumpyArray, NumpyArray2PoolByteArray, NumpyByteArray2NumpyBitArray, NumpyBitArray2NumpyByteArray
from DD.Entity import Entity
import numpy as np

class Material(Entity):
    def __init__(self, json, width, height, scale=2, padding=1):
        super(Material, self).__init__(json)

        self.scale = scale
        self.padding = padding

        bitmap_width = width*self.scale+2*self.padding+1
        bitmap_height = height*self.scale+2*self.padding+1

        bytemap = PoolByteArray2NumpyArray(self._json['bitmap'])
        self.bitmap = NumpyByteArray2NumpyBitArray(bytemap, bitmap_width, bitmap_height)

    def get_json(self):
        json = self._json
        json['bitmap'] = NumpyArray2PoolByteArray(NumpyBitArray2NumpyByteArray(self.bitmap))
        return json

    def pad(self, top, bottom, left, right):
        self.bitmap = np.pad(self.bitmap, ((top*self.scale, bottom*self.scale), (left*self.scale, right*self.scale)), mode='constant', constant_values=0)

    def fliplr(self, width):
        self.bitmap = np.fliplr(self.bitmap)

    def flipud(self, height):
        self.bitmap = np.flipud(self.bitmap)

class Materials(Entity):
    def __init__(self, json, width, height, scale=2):
        super(Materials, self).__init__(json)
        self.scale = scale
        self.layers = [key for key in self._json]
        self.materials = [[Material(material_json, width, height, scale=self.scale) for material_json in self._json[key]] for key in self._json]
        # self.materials = [Material(material_json, width, height, scale=self.scale) for material_json in self._json]

    def get_json(self):
        json = self._json
        json = {key: [material.get_json() for material in layer] for key,layer in zip(self.layers,self.materials)}
        return json

    def pad(self, top, bottom, left, right):
        for layer in self.materials:
            for material in layer:
                material.pad(top, bottom, left, right)

    def crop(self, top, bottom, left, right):
        for layer in self.materials:
            for material in layer:
                material.crop(top, bottom, left, right)

    def fliplr(self, width):
        for layer in self.materials:
            for material in layer:
                material.fliplr(width)
    
    def flipud(self, height):
        for layer in self.materials:
            for material in layer:
                material.flipud(height)

    def transpose(self):
        for layer in self.materials:
            for material in layer:
                material.transpose()

    def rotate(self, angle):
        for layer in self.materials:
            for material in layer:
                material.rotate(angle)
    