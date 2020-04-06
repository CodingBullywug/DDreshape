import copy

from DD.Entity import Entity
from DD.Level import Level

class World(Entity):
    def __init__(self, json):
        super(World, self).__init__(json)
        self.width = self._json['width']
        self.height = self._json['height']

        self.levels = [Level(self._json['levels'][key], self.width, self.height) for key in self._json['levels']]
        self._keys = [key for key in self._json['levels']]

    def get_json(self):
        json = self._json
        json['levels'] = {key:level.get_json() for key,level in zip(self._keys,self.levels)}
        json['height'] = self.height
        json['width'] = self.width
        return json

    def pad(self, top, bottom, left, right):

        self.width += left+right
        self.height += top+bottom

        for level in self.levels:
            level.pad(top, bottom, left, right)

    def fliplr(self, width):
        for level in self.levels:
            level.fliplr(self.width)

    def flipud(self, height):
        for level in self.levels:
            level.flipud(self.height)

    def rot90(self, width, height):
        for level in self.levels:
            level.rot90(self.width, self.height)

        new_width = copy.deepcopy(self.height)
        new_height = copy.deepcopy(self.width)

        self.height = new_height
        self.width = new_width