'''
Created on Jul 24, 2012

@author: mcgillij
'''
from cocos.scene import Scene
from cocos.actions import *
from cocos.layer import Layer, ColorLayer, MultiplexLayer
from cocos.director import director
import pyglet
from pyglet.gl import *
import weakref
from cocos.text import *
from cocos.menu import *

class Model(pyglet.event.EventDispatcher):
    def __init__(self):
        super(Model, self).__init__()
        self.test_val = 5
        status.reset()
        #set test level
        #status.level = something-level

    def set_controller(self, controller):
        self.controller = weakref.ref( controller )

    def start( self ):
        self.set_next_level()
        
    def set_next_level( self ):
        self.controller().resume_controller()
        self.init()  # re-init the object
        # do stuff to load new level
        self.dispatch_event("on_new_level")
    def init(self):
        # set base conditions so we can load a new level
        self.test_val = 5
Model.register_event_type('on_level_complete')
Model.register_event_type('on_new_level')
Model.register_event_type('on_game_over')
Model.register_event_type('on_win')
# add other event types / clicks as events here

class Controller( Layer ):
    is_event_handler = True
    def __init__(self, model):
        super(Controller, self).__init__()
        self.used_key = False
        self.paused = True
        self.model = model
        self.elapsed = 0
        
    def on_key_press(self, k, m):
        if self.paused:
            return False
        if self.used_key:
            return False
        self.used_key = True
        return True
        
        # add some keyboard bindings here
        if k == pyglet.window.key.SPACE:
            print "You pressed Space"
    def pause_controller(self):
        self.paused = True
        self.unschedule(self.step)
    def resume_controller(self):
        self.paused = False
        self.schedule(self.step)
    def step(self, dt):
        self.elapsed += dt
        # add stuff with timesteps here
    def draw(self):
        self.used_key = False

class View(Layer):
    def __init__(self, model, hud):
        super(View, self).__init__()
        width, height = director.get_window_size()
        #setup the view stuff here
        color_layer = ColorLayer( 112, 66, 20, 50, width = width, height=height )
        self.add(color_layer, z=-1)
        self.model = model
        self.hud = hud
        self.model.push_handlers( # win / gameover / various in game effects
                                  self.on_level_complete,
                                  self.on_new_level,
                                  self.on_game_over,
                                  self.on_win,
                                  )
        self.hud.show_message( ' Get ready', self.model.start())

    def on_enter(self):
        super(View, self).on_enter()
        #do sound stuff
        
    def on_exit(self):
        super(View, self).on_exit()
        #stop sound

    def on_level_complete(self):
        #sound stuffs can be done here.
        self.hud.show_message('Level complete', self.model.set_next_level)
        return True

    def on_new_level(self):
        #play new level sound
        self.stop()
        self.do(StopGrid())
        self.rotation = 0
        self.scale = 1
        return True

    def on_game_over(self):
        self.parent.add(GameOver(win=False), z=10)
        return True

    def on_win(self):
        
        self.parent.add(GameOver(win=True), z=10)
        return True

    def draw(self):
        glPushMatrix()
        self.transform()
        #for i in grid draw stuff
        #if self.model.gameobject:
            #self.model.gameobject.draw()
        glPopMatrix()

class GameOver(ColorLayer):
    is_event_handler = True
    def __init__(self, win = False):
        super(GameOver, self).__init__(32, 32, 32, 64)
        width, height = director.get_window_size()

        if win:
            #play win sound
            msg = 'You win!'
        else:
            #play fail sound
            msg = 'Game Over Man! Game Over!'

        label = Label(msg, font_name='Times New Roman', font_size=54, anchor_x='center', anchor_y='center')
        label.position = (width/2.0, height/2.0)
        self.add(label)
        angle = 5
        duration = 0.05
        accel = 2
        rotation = Accelerate(Rotate(angle, duration//2), accel)
        rotation2 = Accelerate(Rotate(-angle*2, duration), accel)
        effect = rotation + (rotation2 + Reverse(rotation2)) * 4 + Reverse(rotation)
        label.do(Repeat(Delay(5) + effect))
        # do high score stuff here

    def on_key_press(self, k, m):
        if (k == pyglet.window.key.ESCAPE):
            director.pop()
            return True

class BackgroundLayer(Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.img = pyglet.resource.image('background.png')
    def draw(self):
        glPushMatrix()
        self.transform()
        self.img.blit(0, 0)
        glPopMatrix()

class ScoreLayer(Layer):
    def __init__(self):
        width, height = director.get_window_size()
        super(ScoreLayer, self).__init__()
        self.add(ColorLayer(32, 32, 32, 32, width=width, height=height), z=-1)
        self.position = (0, height-48)
        self.score = Label('Score:', font_size=36,
                           font_name='Times New Roman',
                           color=(255,255,255,255),
                           anchor_x='left',
                           anchor_y='bottom')
        self.score.position = (0, 0)
        self.add(self.score)
        self.level = Label('Level:', font_size=36,
                         font_name = 'Times New Roman',
                         color = (255, 255, 255, 255),
                         anchor_x = 'left',
                         anchor_y = 'bottom')
        self.add(self.level)

    def draw(self):
        super(ScoreLayer, self).draw()
        self.score.element.text = 'Score:%d' % status.score
        
        level = status.level_index or 0
        self.level.element.text = 'Level:%d', level
        
class MessageLayer(Layer):
    def show_message(self, message, callback=None):
        width, height = director.get_window_size()
        self.message = Label(message, 
                             font_size=52,
                             font_name='Times New Roman',
                             anchor_x='center',
                             anchor_y='center')
        self.message.position = (width/2.0, height)
        self.add(self.message)
        actions = Accelerate(MoveBy( (0,-height/2.0), duration=0.5)) + \
                    Delay(1) +  \
                    Accelerate(MoveBy( (0,-height/2.0), duration=0.5)) + \
                    Hide()

        if callback:
            actions += CallFunc( callback )

        self.message.do( actions )

class HUD(Layer):
    def __init__(self):
        super(HUD, self).__init__()
        self.add(ScoreLayer())
        self.add(MessageLayer(), name='message')

    def show_message(self, message, callback = None):
        self.get('message').show_message(message, callback)
        
__all__ = ['status']
class Status(object):
    def __init__(self):
        self.score = 0
        self.level = None
        self.level_index = None
        
    def reset(self):
        self.score = 0
        self.level = None
        self.level_index = None
status = Status()

class ScoresLayer(ColorLayer):
    FONT_SIZE = 30
    is_event_handler = True
    def __init__(self):
        width, height = director.get_window_size()
        super(ScoresLayer, self).__init__(32, 32, 32, 16, width=width, height=height-86)
        self.font_title = {}
        self.font_title['font_name'] = 'Times New Roman'
        self.font_title['font_size'] = 72
        self.font_title['color'] = (204, 164, 164, 255)
        self.font_title['anchor_x'] = 'center'
        self.font_title['anchor_y'] = 'top'
        title = Label('TEST TITLE', **self.font_title)
        title.position = (width/2.0, height)
        self.add(title, z=1)
        self.table = None

    def on_enter(self):
        super(ScoresLayer, self).on_enter()
        #scores = do score stuffs
        #if self.table:
        #    self.remove_old

    def on_key_press(self, k, m):
        if k in (pyglet.window.key.ENTER, pyglet.window.key.ESCAPE, pyglet.window.key.SPACE):
            self.parent.switch_to(0)
            return True

    def on_mouse_release(self, x, y, b, m):
        self.parent.switch_to(0)
        return True

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
