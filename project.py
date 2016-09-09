from memory_buffer import *
from gfx_atari import *

class Platform():
    name = "Platform name"

class PlatformAtariXl(Platform):
    name = 'Atari 8bit XL/XE'
    avaiable_gfx_modes = [ GfxIndexedTest, GfxAnticMode4MultipleFonts ]

class Project():
    main_memory = MemoryBuffer(65536)
    project_path = 'examples/arkanoid'
    name = "game_name"
    game_data = {
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