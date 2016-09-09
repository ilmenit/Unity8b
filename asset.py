'''
Each asset is:
- savable
- deployable on scene
- has type
- has data
- has dependencies on other assets
- has virtual dependencies on other assets (like gfx editor -> palette)
- has configuration window
- has editor window
'''

class Asset():
    def __init__(self):
        pass

    def placeOnScene(self):
        pass

    def moveToAssets(self):
        pass

    def save(self):
        pass

    def load(self):
        pass