from gfx_atari import *
from playfield_palette import *

class Platform():
    name = "Platform name"

class PlatformAtariXl(Platform):
    name = 'Atari 8bit XL/XE'
    avaiable_gfx_modes = [ GfxIndexedTest, GfxAnticMode4MultipleFonts ]
    supported_assets = [ PlayfieldPalette ]
