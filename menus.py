import pyglet
from cocos.menu import *
from cocos.director import *
from cocos.scene import Scene
from model import Model
from controller import Controller
from view import View
import soundpygame

class OptionsMenu( Menu ):
    def __init__(self):
        super( OptionsMenu, self).__init__('Options') 
        self.select_sound = soundpygame.load('Blip_Select.wav')
        self.font_title['font_name'] = 'Times New Roman'
        self.font_title['font_size'] = 72
        self.font_title['color'] = (204,164,164,255)

        self.font_item['font_name'] = 'Times New Roman',
        self.font_item['color'] = (94,233,239,255)
        self.font_item['font_size'] = 32
        self.font_item_selected['font_name'] = 'Times New Roman'
        self.font_item_selected['color'] = (94,233,239,255)
        self.font_item_selected['font_size'] = 46
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
        super( MainMenu, self).__init__('Dr. Whom!') 
        self.select_sound = soundpygame.load('Blip_Select.wav')
        self.font_title['font_name'] = 'Times New Roman'
        self.font_title['font_size'] = 72
        self.font_title['color'] = (204,164,164,255)

        self.font_item['font_name'] = 'Times New Roman',
        #(32,16,32,255)
        self.font_item['color'] = (94,233,239,255)
        self.font_item['font_size'] = 32
        self.font_item_selected['font_name'] = 'Times New Roman'
        self.font_item_selected['color'] = (94,233,239,255)
        self.font_item_selected['font_size'] = 46

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
    from gamelayers import HUD, PygletParallax
    scene = Scene()
    model = Model()
    controller = Controller(model)
    model.set_controller(controller)
    hud = HUD()
    view = View(model, hud)
    pg = PygletParallax()
    model.set_scroller(pg)
    scene.add(controller, z=1, name='controller')
    scene.add(hud, z=3, name='hud')
    scene.add(pg, z=0, name='background')
    scene.add(view, z=2, name='view')
    return scene