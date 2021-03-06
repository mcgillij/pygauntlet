import pyglet
from pyglet.sprite import Sprite
from pyglet.gl import glPushMatrix, glPopMatrix
from cocos.layer import Layer, ColorLayer
from cocos.text import Label
from cocos.director import director
from cocos.actions import Accelerate, MoveBy, Delay, Hide, CallFunc
from cocos.scenes.transitions import ShuffleTransition
from cocos.scene import Scene
from cocos.layer import MultiplexLayer
from status import status
from menus import MainMenu, OptionsMenu
import hiscore

class PygletParallax(Layer):
    def __init__(self):
        super(PygletParallax, self).__init__()
        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)
        self.bg = Sprite(pyglet.resource.image('parallax1-1024x1900.png'), batch=self.batch, group=self.background)
        self.fg = Sprite(pyglet.resource.image('parallax2-1024x768.png'), batch=self.batch, group=self.foreground)
        self.yspeed = 10
        self.yscroll = 0
        self.yscrollb = 0
        self.bg.x, self.bg.y = 0, 0
        self.fg.x, self.fg.y = 0, 0

    def update(self, dt):
        self.yscroll = self.yscroll + self.yspeed
        if self.yscroll == 320:
            self.yspeed = -1
        if self.yscroll == -960:
            self.yspeed = 2
        self.yscrollb = self.yscroll
        if self.yscrollb < -640:
            self.yscrollb = -640
        if self.yscrollb > 0:
            self.yscrollb = 0
        self.bg.y = self.yscroll
        self.fg.y = self.yscrollb

    def draw(self):
        self.batch.draw()

class BackgroundLayer(Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.img = pyglet.resource.image('background.png')
    def draw(self):
        glPushMatrix()
        self.transform()
        self.img.blit(0, 0)
        glPopMatrix()
        
class IntroLayer(Layer):
    is_event_handler = True
    def __init__(self):
        super(IntroLayer, self).__init__()
        self.img = pyglet.resource.image('background.png')
        self.intro_text = Label('Made by some Asshole:', font_size=24,
                           font_name='Times New Roman',
                           color=(255,255,255,255),
                           anchor_x='left',
                           anchor_y='bottom')
        self.intro_text.position = (0, 0)
        self.add(self.intro_text)
    def draw(self):
        glPushMatrix()
        self.transform()
        self.intro_text.draw()
        self.img.blit(0, 0)
        glPopMatrix()
    def start_game(self):
        scene = Scene()
        scene.add(MultiplexLayer(
                         MainMenu(),
                         OptionsMenu(),
                         HiScoresLayer(),
                         ), z=1)
        scene.add(BackgroundLayer(), z=0)
        director.push(ShuffleTransition(scene, 1.5))
    def on_key_press(self, k, m):
        if k in (pyglet.window.key.ENTER, pyglet.window.key.ESCAPE, pyglet.window.key.SPACE):
            self.start_game()
            return True
    def on_mouse_press(self, x, y, b, m):
        self.start_game()
        return True
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

    def draw(self):
        super(ScoreLayer, self).draw()
        self.score.element.text = 'Score:%d' % status.score

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

class HiScoresLayer(ColorLayer):
    FONT_SIZE = 30
    is_event_handler = True
    def __init__(self):
        width, height = director.get_window_size()
        super(HiScoresLayer, self).__init__(32, 32, 32, 16, width=width, height=height-86)
        self.font_title = {}
        self.font_title['font_name'] = 'Times New Roman'
        self.font_title['font_size'] = 72
        self.font_title['color'] = (204, 164, 164, 255)
        self.font_title['anchor_x'] = 'center'
        self.font_title['anchor_y'] = 'top'
        title = Label('Scores!', **self.font_title)
        title.position = (width/2.0, height)
        self.add(title, z=1)
        self.table = None

    def on_enter(self):
        super(HiScoresLayer, self).on_enter()
        scores = hiscore.hiscore.get()

        if self.table:
            self.remove_old()
        self.table =[]
        for idx,s in enumerate(scores):
            pos= Label( '%d:' % (idx+1), font_name='Times New Roman',
                        font_size=self.FONT_SIZE,
                        anchor_y='top',
                        anchor_x='left',
                        color=(255,255,255,255) )

            name = Label( s[1], font_name='Times New Roman',
                        font_size=self.FONT_SIZE,
                        anchor_y='top',
                        anchor_x='left',
                        color=(255,255,255,255) )

            score = Label( str(s[0]), font_name='Times New Roman',
                        font_size=self.FONT_SIZE,
                        anchor_y='top',
                        anchor_x='right',
                        color=(255,255,255,255) )

            self.table.append( (pos,name,score) )

        self.process_table()
    def remove_old( self ):
        for item in self.table:
            pos,name,score = item
            self.remove(pos)
            self.remove(name)
            self.remove(score)
        self.table = None

    def process_table( self ):
        w,h = director.get_window_size()

        for idx,item in enumerate(self.table):
            pos,name,score = item
            posy = h - 100 - ( (self.FONT_SIZE+15) * idx )
            pos.position=( 5, posy)
            name.position=( 48, posy)
            score.position=( w-150, posy )
            self.add( pos, z=2 )
            self.add( name, z=2 )
            self.add( score, z=2 )

    def on_key_press(self, k, m):
        if k in (pyglet.window.key.ENTER, pyglet.window.key.ESCAPE, pyglet.window.key.SPACE):
            self.parent.switch_to(0)
            return True

    def on_mouse_release(self, x, y, b, m):
        self.parent.switch_to(0)
        return True