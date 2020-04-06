import copy
from DD.utils import PoolVector2Array2NumpyArray, NumpyArray2PoolVector2Array
from DD.Entity import Entity

class Shapes(Entity):
    def __init__(self, json, width, height, scale=256):
        super(Shapes, self).__init__(json)
        self._scale = scale
        self.polygons = [PoolVector2Array2NumpyArray(polygon) for polygon in self._json['polygons']]
        # TODO: Handle walls - appear to always be empty for now

    def get_json(self):
        json = self._json
        json['polygons'] = [NumpyArray2PoolVector2Array(polygon) for polygon in self.polygons]
        return json

    def pad(self, top, bottom, left, right):
        self.polygons = [polygon + [left*self._scale, top*self._scale] for polygon in self.polygons]
            
    def fliplr(self, width):
        for polygon in self.polygons:
            polygon[:,0] = width*self._scale - polygon[:,0]
    
    def flipud(self, height):
        for polygon in self.polygons:
            polygon[:,1] = height*self._scale - polygon[:,1]

    def rot90(self, width, height):
        for polygon in self.polygons:
            polygon = self._rot90_vector(polygon, self._scale, width, height)
            # _polygon = copy.deepcopy(polygon)
            # polygon[:,1] = width*self._scale - _polygon[:,0]
            # polygon[:,0] = _polygon[:,1]