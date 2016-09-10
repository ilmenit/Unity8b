from memory_buffer import *
from gfx_atari import *
from project_platform import *

class Project():
    def __init__(self, name):
        self.main_memory = MemoryBuffer(65536)
        self.path = 'examples/arkanoid'
        self.name = name
        self.platform = PlatformAtariXl()
        self.assets = Assets(self.platform)
        self.game_data = {
            "playfields": [],
            "palettes": [],
            "sounds": [],
            "sprites": [],
            "playfield_data": [],
        }
    def load(self):
        pass

    def save(self):
        pass