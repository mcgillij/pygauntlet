'''
Created on Jul 25, 2012

@author: mcgillij
'''
from cocos.menu import *
from cocos.director import *
import pyglet
from cocos.scene import Scene
from model import Model
from controller import Controller
from view import View
from gamelayers import HUD, BackgroundLayer

class OptionsMenu( Menu ):
    def __init__(self):
        super( OptionsMenu, self).__init__('TITLE!WEUROUOU') 
        #self.select_sound = soundex.load('move.mp3')

        # you can override the font that will be used for the title and the items
        self.font_title['font_name'] = 'Times New Roman'
        self.font_title['font_size'] = 72
        self.font_title['color'] = (204,164,164,255)

        self.font_item['font_name'] = 'Times New Roman',
        self.font_item['color'] = (32,16,32,255)
        self.font_item['font_size'] = 32
        self.font_item_selected['font_name'] = 'Times New Roman'
        self.font_item_selected['color'] = (32,16,32,255)
        self.font_item_selected['font_size'] = 46

        # you can also override the font size and the colors. see menu.py for
        # more info

        # example: menus can be vertical aligned and horizontal aligned
        self.menu_anchor_y = 'center'
        self.menu_anchor_x = 'center'

        items = []

        #self.volumes = ['Mute','10','20','30','40','50','60','70','80','90','100']
        items.append( ToggleMenuItem('Show FPS:', self.on_show_fps, director.show_FPS) )
        items.append( MenuItem('Fullscreen', self.on_fullscreen) )
        items.append( MenuItem('Back', self.on_quit) )
        self.create_menu( items, shake(), shake_back() )

    def on_fullscreen(self):
        director.window.set_fullscreen( not director.window.fullscreen)

    def on_quit(self):
        self.parent.switch_to(0)

    def on_show_fps(self, value):
        director.show_FPS = value

class MainMenu( Menu ):

    def __init__(self):
        super( MainMenu, self).__init__('TEST_TITLE') 

        #self.select_sound = soundex.load('move.mp3')

        # you can override the font that will be used for the title and the items
        # you can also override the font size and the colors. see menu.py for
        # more info
        self.font_title['font_name'] = 'Times New Roman'
        self.font_title['font_size'] = 72
        self.font_title['color'] = (204,164,164,255)

        self.font_item['font_name'] = 'Times New Roman',
        self.font_item['color'] = (32,16,32,255)
        self.font_item['font_size'] = 32
        self.font_item_selected['font_name'] = 'Times New Roman'
        self.font_item_selected['color'] = (32,16,32,255)
        self.font_item_selected['font_size'] = 46


        # example: menus can be vertical aligned and horizontal aligned
        self.menu_anchor_y = 'center'
        self.menu_anchor_x = 'center'

        items = []

        items.append( MenuItem('New Game', self.on_new_game) )
        items.append( MenuItem('Options', self.on_options) )
        items.append( MenuItem('Scores', self.on_scores) )
        items.append( MenuItem('Quit', self.on_quit) )

        self.create_menu( items, shake(), shake_back() )

    def on_new_game(self):
        from cocos.scenes.transitions import FlipAngular3DTransition
        director.push(FlipAngular3DTransition(get_newgame(), 1.5))

    def on_options(self):
        self.parent.switch_to(1)

    def on_scores(self):
        self.parent.switch_to(2)

    def on_quit(self):
        pyglet.app.exit()
        

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
    pass