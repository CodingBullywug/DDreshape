from DD.utils import PoolByteArray2NumpyArray, NumpyArray2PoolByteArray, NumpyByteArray2NumpyBitArray, NumpyBitArray2NumpyByteArray
from DD.Entity import Entity
import numpy as np

class Cave(Entity):
    def __init__(self, json, width, height, scale=4, padding=1):
        super(Cave, self).__init__(json)
        
        self._scale = scale
        self.padding = padding

        bitmap_width = width*self._scale+2*self.padding+1
        bitmap_height = height*self._scale+2*self.padding+1

        bytemap = PoolByteArray2NumpyArray(self._json['bitmap'])
        self.bitmap = NumpyByteArray2NumpyBitArray(bytemap, bitmap_width, bitmap_height)

    def get_json(self):
        json = self._json
        json['bitmap'] = NumpyArray2PoolByteArray(NumpyBitArray2NumpyByteArray(self.bitmap))
        return json

    def pad(self, top, bottom, left, right):
        self.bitmap = np.pad(self.bitmap, ((top*self._scale, bottom*self._scale), (left*self._scale, right*self._scale)), mode='constant', constant_values=0)

    def crop(self, top, bottom, left, right):
        # self.bitmap = self.bitmap[top*self._scale:self.bitmap.shape[0]-bottom*self._scale,left*self._scale:self.bitmap.shape[1]-right*self._scale]
        self.bitmap = self._crop_map_safe(self.bitmap, top, bottom, left, right, self._scale)

    def fliplr(self, width):
        self.bitmap = np.fliplr(self.bitmap)
    
    def flipud(self, height):
        self.bitmap = np.flipud(self.bitmap)

    def rot90(self, width, height):
        self.bitmap = self._rot90_map(self.bitmap)
        # self.bitmap = np.rot90(self.bitmap, k=1)

    def rot180(self, width, height):
        self.bitmap = self._rot180_map(self.bitmap)
        # self.bitmap = np.rot90(self.bitmap, k=2)

    def rot270(self, width, height):
        self.bitmap = self._rot270_map(self.bitmap)
        # self.bitmap = np.rot90(self.bitmap, k=3)
