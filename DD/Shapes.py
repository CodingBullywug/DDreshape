from DD.utils import PoolVector2Array2NumpyArray, NumpyArray2PoolVector2Array
from DD.Entity import Entity

class Shapes(Entity):
    def __init__(self, json, width, height, scale=256):
        super(Shapes, self).__init__(json)
        self.scale = scale
        self.polygons = [PoolVector2Array2NumpyArray(polygon) for polygon in self._json['polygons']]
        # TODO: Handle walls - appear to always be empty for now

    def get_json(self):
        json = self._json
        json['polygons'] = [NumpyArray2PoolVector2Array(polygon) for polygon in self.polygons]
        return json

    def pad(self, top, bottom, left, right):
        self.polygons = [polygon + [left*self.scale, top*self.scale] for polygon in self.polygons]
            
    def fliplr(self, width):
        for polygon in self.polygons:
            polygon[:,0] = width*self.scale - polygon[:,0]
    
    def flipud(self, height):
        for polygon in self.polygons:
            polygon[:,1] = height*self.scale - polygon[:,1]