import copy

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

    def transpose(self):
        raise NotImplementedError('Transposing has not yet been implemented for ' + type(self).__name__ + '.')

    def rotate(self, angle):
        raise NotImplementedError('Rotation has not yet been implemented for ' + type(self).__name__ + '.')


    