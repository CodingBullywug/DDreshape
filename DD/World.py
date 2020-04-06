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

    def fliplr(self):
        for level in self.levels:
            level.fliplr(self.width)

    def flipud(self):
        for level in self.levels:
            level.flipud(self.height)
        pass
