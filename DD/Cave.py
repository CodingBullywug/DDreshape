from DD.utils import PoolByteArray2NumpyArray, NumpyArray2PoolByteArray, NumpyByteArray2NumpyBitArray, NumpyBitArray2NumpyByteArray
from DD.Entity import Entity
import numpy as np

class Cave(Entity):
    def __init__(self, json, width, height, scale=4, padding=1):
        super(Cave, self).__init__(json)
        
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