import copy
import numpy as np

class Entity(object):
    def __init__(self, json):
        self._json = copy.deepcopy(json)

    def get_json(self):
        raise NotImplementedError('Getting the json has not yet been implemented for ' + type(self).__name__ + '.')

    def pad(self, top, bottom, left, right):
        raise NotImplementedError('Padding has not yet been implemented for ' + type(self).__name__ + '.')

    def crop(self, top, bottom, left, right):
        raise NotImplementedError('Cropping has not yet been implemented for ' + type(self).__name__ + '.')

    def fliplr(self, width):
        raise NotImplementedError('Flipping left-right has not yet been implemented for ' + type(self).__name__ + '.')

    def flipud(self, height):
        raise NotImplementedError('Flipping up-down has not yet been implemented for ' + type(self).__name__ + '.')

    def rot90(self, width, height):
        raise NotImplementedError('90 degree rotation has not yet been implemented for ' + type(self).__name__ + '.')

    def rot180(self, width, height):
        self.rot90(width, height)
        self.rot90(width, height)
    
    def rot270(self, width, height):
        self.rot90(width, height)
        self.rot90(width, height)
        self.rot90(width, height)

    def transpose(self, width, height, anti=False):
        self.rot90(width, height)
        if (anti):
            self.fliplr(width)
        else:
            self.flipud(height)

    def rotate(self, angle, width, height):
        raise NotImplementedError('Rotation has not yet been implemented for ' + type(self).__name__ + '.')

    def _crop_map_safe(self, bmap, top, bottom, left, right, scale=1):
        return bmap[top*scale:bmap.shape[0]-bottom*scale,left*scale:bmap.shape[1]-right*scale]

    def _rot90_map(self, bmap):
       return np.rot90(bmap, k=1)

    def _rot180_map(self, bmap):
        return np.rot90(bmap, k=2)

    def _rot270_map(self, bmap):
        return np.rot90(bmap, k=3)

    def _rot90_point(self, point, scale, width, height):
        _point = copy.deepcopy(point)
        point[1] = width*scale - point[0]
        point[0] = _point[1]
        return point

    def _rot90_vector(self, vector, scale, width, height):
        _vector = copy.deepcopy(vector)
        vector[:,1] = width*scale - _vector[:,0]
        vector[:,0] = _vector[:,1]
        return vector

    def _rotate_vector(self, vector, angle):
        R = np.asarray([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)]])
        return np.dot(R, vector.T).T