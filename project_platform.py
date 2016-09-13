from gfx_atari import *
from asset_playfield_palette import *

class Platform():
    name = "Platform name"

class PlatformAtariXl(Platform):
    name = 'Atari 8bit XL/XE'
    supported_assets = [AssetPlayfieldPalette, GfxIndexedAsset]
