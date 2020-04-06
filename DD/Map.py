from DD.Entity import Entity
from DD.Header import Header
from DD.World import World

class Map(Entity):

    def __init__(self, json):
        super(Map, self).__init__(json)

        self.header = Header(self._json['header'])
        self.world = World(self._json['world'])

    def get_json(self):
        json = self._json
        json['header'] = self.header.get_json()
        json['world'] = self.world.get_json()
        return json

    def pad(self, top, bottom, left, right):
        self.header.pad(top, bottom, left, right)
        self.world.pad(top, bottom, left, right)

    def fliplr(self):
        self.header.fliplr(self.world.width)
        self.world.fliplr(self.world.width)

    def flipud(self):
        self.header.flipud(self.world.height)
        self.world.flipud(self.world.height)
    
    def rot90(self):
        self.header.rot90(self.world.width, self.world.height)
        self.world.rot90(self.world.width, self.world.height)

    def rot180(self):
        self.header.rot180(self.world.width, self.world.height)
        self.world.rot180(self.world.width, self.world.height)

    def rot270(self):
        self.header.rot270(self.world.width, self.world.height)
        self.world.rot270(self.world.width, self.world.height)
    
    def transpose(self):
        self.header.transpose(self.world.width, self.world.height)
        self.world.transpose(self.world.width, self.world.height)