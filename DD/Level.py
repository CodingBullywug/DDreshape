from DD.Entity import Entity

from DD.Cave import Cave
from DD.Lights import Lights
from DD.Materials import Materials
from DD.Objects import Objects
from DD.Paths import Paths
from DD.Portals import Portals
from DD.Shapes import Shapes
from DD.Terrain import Terrain
from DD.Tiles import Tiles
from DD.Walls import Walls
from DD.Water import Water

class Level(Entity):

    def __init__(self, json, width, height):
        super(Level, self).__init__(json)
        self.width = width
        self.height = height

        self.entities =  [('cave', Cave(self._json['cave'], self.width, self.height)),
                          ('lights',Lights(self._json['lights'], self.width, self.height)),
                          ('materials',Materials(self._json['materials'], self.width, self.height)),
                          ('objects',Objects(self._json['objects'], self.width, self.height)),
                          ('portals',Portals(self._json['portals'], self.width, self.height)),
                          ('paths',Paths(self._json['paths'], self.width, self.height)),
                          ('shapes',Shapes(self._json['shapes'], self.width, self.height)),
                          ('terrain', Terrain(self._json['terrain'], self.width, self.height)),
                          ('tiles', Tiles(self._json['tiles'], self.width, self.height)),
                          ('walls', Walls(self._json['walls'], self.width, self.height)),
                          ('water', Water(self._json['water'], self.width, self.height))]

    def pad(self, top, bottom, left, right):
        [entity.pad(top, bottom, left, right) for _, entity in self.entities]

    def get_json(self):
        json = self._json

        for key, entity in self.entities:
            json[key] = entity.get_json() 
        return json
        

