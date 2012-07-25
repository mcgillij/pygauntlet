'''
Created on Jul 25, 2012

@author: mcgillij
'''

from cocos.scene import Scene
from cocos.layer import MultiplexLayer
from cocos.director import director
from model import Model
from controller import Controller
from view import View
from gamelayers import HUD, BackgroundLayer, ScoresLayer
from menus import MainMenu, OptionsMenu
import pyglet

def get_newgame():
    scene = Scene()
    model = Model()
    controller = Controller(model)
    model.set_controller(controller)
    hud = HUD()
    view = View(model, hud)
    scene.add(controller, z=1, name='controller')
    scene.add(BackgroundLayer(), z=0, name='background')
    scene.add(view, z=2, name='view')
    return scene

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
