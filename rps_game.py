'''
Created on Jul 25, 2012

@author: mcgillij
'''

from cocos.scene import Scene
from cocos.layer import MultiplexLayer
from cocos.director import director
from gamelayers import BackgroundLayer, ScoresLayer
from menus import MainMenu, OptionsMenu
import pyglet


if __name__ == '__main__':
    pyglet.resource.path.append('assets')
    pyglet.resource.reindex()
    pyglet.font.add_directory('assets')
    director.init(resizable = True, width=600, height=720)
    scene = Scene()
    scene.add(MultiplexLayer(
                             MainMenu(),
                             OptionsMenu(),
                             ScoresLayer(),
                             ), z=1)
    scene.add(BackgroundLayer(), z=0)
    director.run(scene)
