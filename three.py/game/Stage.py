## Stage - provice a method of interacting with scenes in more of a game context
from core import Scene
class Stage(object):
    def __init__(self):
        self.scene= Scene()

    def add(self,player):
        self.scene.add(player.mesh)
