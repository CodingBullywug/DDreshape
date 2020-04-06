from DD.Entity import Entity
from DD.Header import Header
from DD.World import World

class Map(Entity):

    def __init__(self, json):
        super(Map, self).__init__(json)

        self.header = Header(self._json['header'])
        self.world = World(self._json['world'])

        # TODO: Handle header

    def pad(self, top, bottom, left, right):
        self.header.pad(top, bottom, left, right)
        self.world.pad(top, bottom, left, right)

    def get_json(self):
        json = self._json
        json['header'] = self.header.get_json()
        json['world'] = self.world.get_json()
        return json